from flask import Flask, request, jsonify, render_template, send_from_directory
import pyttsx3
import tempfile
import os
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob
import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/audio"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load NLTK data
nltk.download('punkt')

# Load Pegasus model & tokenizer
pegasus_model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(pegasus_model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(pegasus_model_name)

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def extractive_summary(text, num_sentences=3):
    """Extracts key sentences using TextRank algorithm."""
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    
    vectorizer = TfidfVectorizer(stop_words="english")
    sentence_vectors = vectorizer.fit_transform(sentences)
    similarity_matrix = sentence_vectors * sentence_vectors.T  # Corrected cosine similarity
    
    nx_graph = nx.from_numpy_array(similarity_matrix.toarray())
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    return " ".join([s[1] for s in ranked_sentences[:num_sentences]])

def abstractive_summary(text):
    """Uses Pegasus for abstractive summarization."""
    inputs = pegasus_tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = pegasus_model.generate(
        inputs["input_ids"], max_length=100, min_length=30, num_beams=8,
        length_penalty=1.2, repetition_penalty=1.2, early_stopping=True
    )
    return pegasus_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def filter_by_sentiment(text, sentiment="negative"):
    sentences = sent_tokenize(text)
    filtered_sentences = [
        sentence for sentence in sentences if (
            (TextBlob(sentence).sentiment.polarity < 0 and sentiment == "negative") or
            (TextBlob(sentence).sentiment.polarity > 0 and sentiment == "positive")
        )
    ]
    return ' '.join(filtered_sentences) if filtered_sentences else text

def text_to_speech(text):
    """Convert text to speech and return audio file path."""
    filename = os.path.join(app.config["UPLOAD_FOLDER"], "summary.mp3")
    tts_engine.save_to_file(text, filename)
    tts_engine.runAndWait()
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get("text", "").strip()
    num_sentences = int(data.get("num_sentences", 3))
    summary_type = data.get("summary_type", "Extractive")
    context_filter = data.get("context_filter", "None")
    output_format = data.get("output_format", "Text")

    if not text:
        return jsonify({"error": "Please provide some text to summarize."}), 400

    if context_filter == "Negative Sentiment":
        text = filter_by_sentiment(text, "negative")
    elif context_filter == "Positive Sentiment":
        text = filter_by_sentiment(text, "positive")

    summary = extractive_summary(text, num_sentences) if summary_type == "Extractive" else abstractive_summary(text)
    audio_file = text_to_speech(summary)

    response = {"summary": summary, "audio_file": f"/static/audio/summary.mp3"}
    if output_format == "Markdown":
        response["summary"] = f"**Summary:** {summary}"
    elif output_format == "JSON":
        response = {"summary": summary}
    
    return jsonify(response)

@app.route('/static/audio/<filename>')
def get_audio(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
