from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the LLM-powered Flask App!"

# Load a local LLM model
llm_pipeline = pipeline("text-generation", model="distilgpt2")

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    query = data.get("query", "")

    # Query the local model
    response = llm_pipeline(query, max_length=50, num_return_sequences=1)
    answer = response[0]["generated_text"]

    return jsonify({"query": query, "response": answer})

if __name__ == "__main__":
    # Use environment variables for debug and port
    debug = os.getenv("DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 8501))
    app.run(host="0.0.0.0", port=port, debug=debug)
