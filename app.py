from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def query_hf(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    return "Welcome to the Hugging Face Inference API-powered Flask App!"

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    payload = {"inputs": query, "parameters": {"max_length": 50, "num_return_sequences": 1}}
    api_response = query_hf(payload)

    if isinstance(api_response, dict) and "error" in api_response:
        return jsonify({"error": api_response["error"]}), 500

    answer = api_response[0]["generated_text"] if api_response else "No response generated."

    return jsonify({"query": query, "response": answer})

if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 8501))
    app.run(host="0.0.0.0", port=port, debug=debug)
