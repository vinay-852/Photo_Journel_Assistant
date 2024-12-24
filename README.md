---
title: Photo Journel Assistant
emoji: 📉
colorFrom: purple
colorTo: green
sdk: streamlit
sdk_version: 1.40.2
app_file: app.py
pinned: false
license: mit
short_description: Photo Journel Assistant
---
# Photo Journal Assistant

The **Photo Journal Assistant** is a Streamlit-based app that helps you transform your daily experiences into personalized journal entries using photos. Upload your images, and the app will generate captions, extract metadata, and craft a cohesive and reflective journal entry. 

---

## Features

### 1. **Image Caption Generation**
   - Uses the **BLIP Image Captioning** model from Salesforce to generate meaningful captions for uploaded images.
   - Captions are tailored based on a given prompt, such as describing the image's essence or context.

### 2. **Metadata Extraction**
   - Extracts EXIF metadata from images, such as:
     - **Date Taken**: The timestamp when the photo was captured.
     - **Location**: Latitude and longitude if GPS data is available.
   - Displays human-readable formats for easy understanding.

### 3. **Journal Entry Generation**
   - Combines image captions and metadata to create a reflective, personalized journal entry.
   - Powered by **Google Gemini AI**, it crafts immersive and engaging narratives using a creative writing prompt.

### 4. **Downloadable Output**
   - Outputs the journal entry in plain text format.
   - Users can download and save their generated journals.

### 5. **Live Preview**
   - Try the app live: [Photo Journal Assistant (Live)](https://vinay-pepakayala-ai-photo-journel-assistant.hf.space)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/photo-journal-assistant.git
   cd photo-journal-assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Google Generative AI API key:
     ```env
     GENAI_API_KEY=your_api_key
     ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Launch the app in your browser.
2. Upload your photos in supported formats (**JPG, JPEG, PNG**).
3. View the generated captions and metadata for each photo.
4. Read and download your personalized journal entry.

---

## How It Works

1. **Image Captioning**:
   - The BLIP model generates captions based on the content of the image and a specified prompt.

2. **Metadata Extraction**:
   - Extracts EXIF metadata, including GPS coordinates.
   - Decodes GPS data into a human-readable location format.

3. **Journal Writing**:
   - Google Gemini AI synthesizes captions and metadata into a cohesive narrative.
   - Reflects on transitions, emotions, and highlights of the day.

---

## Dependencies

- **Streamlit**: For building the user interface.
- **Pillow**: For image processing and metadata extraction.
- **Transformers**: For loading and running the BLIP model.
- **google-generativeai**: For accessing Google Gemini AI capabilities.
- **Python-dotenv**: For managing API keys securely.

---

## Contribution

Feel free to submit pull requests or open issues for improvements and bug fixes. Let’s make journaling with AI even better!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
