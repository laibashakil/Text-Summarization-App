# Text Summarization App

This project is a Flask-based Text Summarization App that supports both extractive and abstractive summarization. It provides contextual filtering, adaptive summary generation, multi-format outputs, and text-to-speech functionality.

## Features
- **Extractive Summarization:** Uses the TextRank algorithm to extract key sentences from the input text.
- **Abstractive Summarization:** Utilizes the Pegasus transformer model to generate rewritten summaries.
- **Contextual Summarization:** Allows filtering by sentiment (positive/negative) before summarization.
- **Adaptive Summary Generation:** Dynamically adjusts summaries based on input text structure and user-defined constraints.
- **Multi-Format Output:** Supports text, JSON, and Markdown output.
- **Text-to-Speech (TTS):** Converts summaries into speech and provides an audio file.
- **User-Friendly UI:** A Bootstrap-powered web interface for easy interaction.
- **API Endpoint:** Allows programmatic access with JSON requests and responses.
- **Loading Spinner:** Displays a visual cue while processing the request.

## Setup Instructions

### Prerequisites
Ensure you have Python 3.8+ installed and run the following:

```bash
pip install -r requirements.txt
```

### Running the Application
To start the Flask server, run:

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000/`.

## API Usage
### Endpoint: `/summarize`
**Method:** `POST`

**Request Body (JSON):**
```json
{
  "text": "Your input text here.",
  "num_sentences": 3,
  "summary_type": "Extractive", 
  "context_filter": "None",
  "output_format": "Text"
}
```

**Response (Example for Text Output):**
```json
{
  "summary": "Key sentences from the input text."
}
```

**Response (Example for Audio Output):**
```json
{
  "summary": "Key sentences from the input text.",
  "audio_file": "/static/summary.mp3"
}
```

## Folder Structure
```
Text-Summarization-App/
│── app.py               # Main Flask application
│── templates/
│   ├── index.html       # Frontend UI
│── static/
│   ├── summary.mp3      # Temporary audio files (ignored in git)
│── requirements.txt     # Dependencies
│── README.md            # This file
│── .gitignore           # Ignored files
```

## Notes
- The application dynamically generates an audio file for summaries with TTS enabled.
- The `.gitignore` file ensures temporary files and virtual environment dependencies are not tracked.

For any issues, feel free to contribute or report bugs!
