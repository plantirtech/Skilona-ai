from flask import Flask, request, jsonify
import os
import google.generativeai as genai
import requests
import base64

app = Flask(__name__)

# Load API keys from environment variables (secure!)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CX_ID")  # Google Custom Search Engine ID

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model_text = genai.GenerativeModel("gemini-pro")
model_vision = genai.GenerativeModel("gemini-pro-vision")

# Health check
@app.route("/", methods=["GET"])
def home():
    return "Skilona-ai Backend is Running"

# Text AI questions
@app.route("/text", methods=["POST"])
def ask_text():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = model_text.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Skin image analysis
@app.route("/vision", methods=["POST"])
def analyze_skin():
    image_file = request.files.get("image")
    prompt = request.form.get("prompt", "")
    if not image_file:
        return jsonify({"error": "No image uploaded"}), 400
    try:
        img_bytes = image_file.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        response = model_vision.generate_content([prompt, {"mime_type":"image/jpeg","data":img_b64}])
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Google Search for skincare products and routines
@app.route("/search", methods=["POST"])
def google_search():
    query = request.json.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CUSTOM_SEARCH_ENGINE_ID}"
        result = requests.get(url).json()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)