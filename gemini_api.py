from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyBDUyo-bQHcvndbqxy5wLUDVV6-ZrrgFUs")

@app.route("/", methods=["GET"])
def home():
    return "Gemini API is running!"

@app.route("/generate", methods=["POST"])
def generate_steps():
    try:
        data = request.get_json()
        goal = data.get("goal", "")
        prompt = f"Give me 5 step-by-step instructions to achieve this goal:\n{goal}"

        # Use model name as "gemini-pro" directly — not with "models/"
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(prompt)

        return jsonify({"steps": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
