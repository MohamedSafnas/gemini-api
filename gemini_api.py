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
        print("📥 Received data:", data)

        goal = data.get("goal", "")
        if not goal:
            return jsonify({"error": "Goal not provided"}), 400

        print("🎯 Goal:", goal)

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Suggest 5 step-by-step instructions to achieve this goal: {goal}")
        print("✅ Response:", response)

        return jsonify({"steps": response.text})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
