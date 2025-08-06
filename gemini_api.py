from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key="AIzaSyBDUyo-bQHcvndbqxy5wLUDVV6-ZrrgFUs")  # Replace this with your real key

@app.route("/generate", methods=["POST"])
def generate_steps():
    data = request.get_json()
    goal = data.get("goal", "")

    if not goal:
        return jsonify({"error": "Goal not provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Suggest 5 step-by-step instructions to achieve this goal: {goal}")
        return jsonify({"steps": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
