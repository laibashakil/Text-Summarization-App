from flask import Flask, request, jsonify, render_template
import pyttsx3
import tempfile
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

# Initialize Flask app
app = Flask(__name__)

# Load NLTK data
nltk.download('punkt')

# Load Pegasus model & tokenizer
pegasus_model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(pegasus_model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(pegasus_model_name)

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# ---- HELPER FUNCTIONS ----

def extractive_summary(text, num_sentences=3):
    """Extracts key sentences based on importance rather than just the first N sentences."""
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text  # If text is too short, return as is

    sorted_sentences = sorted(sentences, key=len, reverse=True)[:num_sentences]
    
    return ' '.join(sorted_sentences)

def abstractive_summary(text):
    """Uses Pegasus for abstractive summarization with optimized parameters."""
    inputs = pegasus_tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = pegasus_model.generate(
        inputs["input_ids"],
        max_length=100,  # Allows richer summaries
        min_length=30,
        num_beams=8,  # Higher beams for better quality
        length_penalty=1.2,  # Encourages longer, well-formed summaries
        repetition_penalty=1.2,  # Reduces redundancy
        early_stopping=True
    )

    output = pegasus_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

def filter_by_sentiment(text, sentiment="negative"):
    """Filter sentences based on sentiment (positive or negative)."""
    sentences = sent_tokenize(text)
    filtered_sentences = [
        sentence for sentence in sentences if (
            (TextBlob(sentence).sentiment.polarity < 0 and sentiment == "negative") or
            (TextBlob(sentence).sentiment.polarity > 0 and sentiment == "positive")
        )
    ]
    return ' '.join(filtered_sentences)

def text_to_speech(text):
    """Convert text to speech and save to an audio file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts_engine.save_to_file(text, fp.name)
        tts_engine.runAndWait()
        return fp.name

# ---- ROUTES ----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get("text", "").strip()
    num_sentences = int(data.get("num_sentences", 3))
    summary_type = data.get("summary_type", "Extractive")  # Extractive or Abstractive
    context_filter = data.get("context_filter", "None")
    output_format = data.get("output_format", "Text")

    if not text:
        return jsonify({"error": "Please provide some text to summarize."}), 400

    # Apply sentiment filtering if needed
    if context_filter == "Negative Sentiment":
        text = filter_by_sentiment(text, "negative")
    elif context_filter == "Positive Sentiment":
        text = filter_by_sentiment(text, "positive")

    # Choose summary type
    if summary_type == "Extractive":
        summary = extractive_summary(text, num_sentences)
    elif summary_type == "Abstractive":
        summary = abstractive_summary(text)
    else:
        return jsonify({"error": "Invalid summary type selected."}), 400

    # Format the output
    response = {"summary": summary}
    if output_format == "Markdown":
        response["summary"] = f"**Summary:** {summary}"
    elif output_format == "Voice":
        audio_file = text_to_speech(summary)
        response["audio_file"] = audio_file

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
