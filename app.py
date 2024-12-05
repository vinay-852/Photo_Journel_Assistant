import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from transformers import BlipProcessor, BlipForConditionalGeneration
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI API
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Chat model configuration
chat_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 2048,  # Limit to a manageable size
    "response_mime_type": "text/plain",
}

# Initialize the Generative AI model
ai_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=chat_config,
)

# Load BLIP model for caption generation
@st.cache_resource
def load_image_caption_model():
    caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    return caption_processor, caption_model

# Generate image captions
def create_image_caption(image_file, prompt="This is an image of"):
    try:
        processor, model = load_image_caption_model()
        image = Image.open(image_file).convert("RGB")
        inputs = processor(image, prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {e}"

# Extract metadata from an image
def extract_image_metadata(image_file):
    try:
        image = Image.open(image_file)
        exif_data = image._getexif()
        
        # Handle missing metadata
        if not exif_data:
            return {"DateTaken": "Unknown", "Location": "Unknown"}
        
        # Parse DateTaken and Location
        metadata = {}
        metadata["DateTaken"] = exif_data.get(36867, "Unknown")  # DateTimeOriginal
        gps_info = exif_data.get(34853)  # GPSInfo
        if gps_info:
            def decode_gps(coord):
                d, m, s = coord
                return d + m / 60.0 + s / 3600.0
            
            lat = gps_info.get(2)
            lon = gps_info.get(4)
            if lat and lon:
                lat_ref = gps_info.get(1, "N")
                lon_ref = gps_info.get(3, "E")
                lat_decimal = decode_gps(lat) * (-1 if lat_ref == "S" else 1)
                lon_decimal = decode_gps(lon) * (-1 if lon_ref == "W" else 1)
                metadata["Location"] = f"Latitude: {lat_decimal:.6f}, Longitude: {lon_decimal:.6f}"
            else:
                metadata["Location"] = "Unknown"
        else:
            metadata["Location"] = "Unknown"
        
        return metadata
    except Exception as e:
        return {"DateTaken": "Unknown", "Location": f"Error extracting metadata: {e}"}


def create_journal_entry(image_captions, image_metadata):
    try:
        structured_prompt = (
            "You are a creative journal-writing assistant. Based on the photo captions and context, craft a brief yet engaging "
            "journal entry that weaves the events into a cohesive story. Focus on maintaining a natural sequence by deducing the "
            "time of day (morning, afternoon, evening) and transitions between locations. Use a reflective and personal tone, "
            "capturing emotions and highlights without unnecessary details. If time or location is missing, focus on the essence "
            "of the moment to maintain flow. Keep the journal succinct and immersive."
        )
        
        # Combine captions and metadata
        events = []
        previous_location = None
        for i, (caption, meta) in enumerate(zip(image_captions, image_metadata)):
            location = meta.get("Location", "Unknown")
            if location != "Unknown":
                if previous_location and previous_location != location:
                    travel_info = "It felt like a journey between places."
                else:
                    travel_info = "I remained in the same surroundings."
                previous_location = location
            else:
                travel_info = ""
            
            event_description = f"Photo {i+1}: {caption}. {travel_info}"
            events.append(event_description)
        
        user_input = f"{structured_prompt}\n\nHere are the key moments from my day:\n" + "\n".join(events)

        # Start chat session
        chat_session = ai_model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [user_input],
                }
            ]
        )

        # Generate the response
        response = chat_session.send_message(user_input).text
        return response
    except Exception as e:
        return f"Error generating journal entry: {e}"


# Streamlit app layout
st.title("Photo Journal Assistant")
st.markdown(
    """
    **Welcome to the Photo Journal Assistant!**  
    Upload your photos, and this tool will help you:  
    - **Generate meaningful captions** for each photo.  
    - **Extract metadata** like date and location (if available).  
    - **Create a beautifully written journal entry** combining all details.  
    """
)

# File uploader for images
uploaded_photos = st.file_uploader(
    "Upload your photos (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if uploaded_photos:
    st.subheader("Processing Your Photos")
    image_captions = []
    metadata_records = []

    for photo in uploaded_photos:
        try:
            with st.expander(f"Photo: {photo.name}"):
                st.image(photo, caption=photo.name, use_column_width=True)
                
                # Generate caption
                caption = create_image_caption(photo)
                image_captions.append(caption)
                st.write(f"**Caption:** {caption}")
                
                # Extract metadata
                metadata = extract_image_metadata(photo)
                metadata_records.append(metadata)
                st.write(f"**Metadata:** Date Taken - {metadata['DateTaken']}, Location - {metadata['Location']}")
        except Exception as e:
            st.error(f"Error processing {photo.name}: {e}")

    # Generate the journal entry
    if image_captions and metadata_records:
        st.subheader("Your Generated Journal Entry")
        with st.spinner("Crafting your journal entry..."):
            journal_output = create_journal_entry(image_captions, metadata_records)
        st.text_area("Journal Entry", value=journal_output, height=300)
        
        # Option to download the journal entry
        st.download_button(
            label="Download Journal Entry as Text",
            data=journal_output,
            file_name="photo_journal_entry.txt",
            mime="text/plain",
        )
