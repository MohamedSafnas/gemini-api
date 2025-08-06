from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Set your API key
GOOGLE_API_KEY = "AIzaSyBDUyo-bQHcvndbqxy5wLUDVV6-ZrrgFUs"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

@app.route('/generate-steps', methods=['POST'])
def generate_steps():
    data = request.get_json()
    goal = data.get("goal")

    if not goal:
        return jsonify({"error": "Goal not provided"}), 400

    prompt = f"Suggest 5 clear step-by-step instructions to achieve this goal: {goal}"

    try:
        response = model.generate_content(prompt)
        return jsonify({"steps": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
