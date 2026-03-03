from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow requests from MIT App Inventor

# ── PUT YOUR ANTHROPIC API KEY HERE ──
ANTHROPIC_API_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 1000,
                "system": "You are a helpful and friendly AI assistant. Be concise and clear.",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()
        reply = result["content"][0]["text"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "AI Chatbot Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)