# Text Summarization App

This project is a Flask-based Text Summarization App that supports both extractive and abstractive summarization. It provides contextual filtering, adaptive summary generation, multi-format outputs, and text-to-speech functionality.

## **Features**

### **Summarization Types**

-   **Extractive Summarization:** Uses the **TextRank algorithm** (via `sumy`) to extract key sentences.
-   **Abstractive Summarization:** Utilizes **Google's Pegasus Transformer Model** (`transformers` library) to generate rewritten summaries.

### **Context-Aware Summarization**

-   **Sentiment-Based Filtering:** Summaries can be filtered to show only **positive** or **negative** sentiments using `VADER Sentiment Analysis`.

### **Output Formats**

-   **Plain Text:** Standard text output.
-   **JSON:** Structured output for API use.
-   **Markdown:** Returns a formatted summary.
-   **API Response:** Raw JSON output for direct API usage.

### **Additional Features**

-   **Text-to-Speech (TTS):** Converts the summary into speech using `gTTS` and provides an audio file.
-   **Bootstrap UI:** A responsive and user-friendly web interface.
-   **API Endpoint:** Programmatic access for automation.
-   **Loading Spinner:** Displays a visual cue while processing.

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
## Screenshots
### 1️⃣ Application UI
![image](https://github.com/user-attachments/assets/b87c3432-a862-4152-b679-091b89a3079a)

### 2️⃣ Example Summary Outputs
![image](https://github.com/user-attachments/assets/110cd00a-59c3-4bf3-9f13-7f97278dc330)
![image](https://github.com/user-attachments/assets/e66b2201-e702-4f63-a684-6a2a2e1f7300)
![image](https://github.com/user-attachments/assets/8b7fb638-754a-4fef-95f5-a8092145c7f9)

### 3️⃣ API Usage via cURL
![image](https://github.com/user-attachments/assets/df8e82e5-a36c-46d9-88e0-90690a26faba)

## Notes
- The application dynamically generates an audio file for summaries with TTS enabled.
- The `.gitignore` file ensures temporary files and virtual environment dependencies are not tracked.

For any issues, feel free to contribute or report bugs!
