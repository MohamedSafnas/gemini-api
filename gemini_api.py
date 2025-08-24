from flask import Flask, request, jsonify
import google.generativeai as genai
import os


from datetime import datetime, timedelta


app = Flask(__name__)

genai.configure(api_key="AIzaSyBDUyo-bQHcvndbqxy5wLUDVV6-ZrrgFUs")  

@app.route("/", methods=["GET"])
def home():
    return "Gemini API is running!"

@app.route("/generate", methods=["POST"])
def generate_steps():
    try:
        data = request.get_json()
        print("Received data:", data)

        goal = data.get("goal", "")
        if not goal:
            return jsonify({"error": "Goal not provided"}), 400

        print("Goal:", goal)

    
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(f"Suggest 5 step-by-step instructions to achieve this goal: {goal}")

        print("Response:", response.text)

        return jsonify({"steps": response.text})

    except Exception as e:
        print("Exception:", e)
        return jsonify({"error": str(e)}), 500
    


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Goal-based prediction inputs
    goal_name = data.get("goalName")
    completion = data.get("completionPercentage")
    created_date = data.get("createdDate")  

    # Custom prediction inputs
    title = data.get("title")
    frequency = data.get("frequency")  # "daily", "weekly", "monthly"
    duration = data.get("duration")    # hours per frequency

    if title and frequency and duration:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"If someone does '{title}' for {duration} hours {frequency}, "
                f"what are the possible advantages and disadvantages? "
                f"Explain in briefly."
            )
            response = model.generate_content(prompt)

            if response.candidates and response.candidates[0].content.parts:
                 analysis_text = response.candidates[0].content.parts[0].text
            else:
                 analysis_text = "No prediction generated."

            return jsonify({"prediction": analysis_text})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Goal-based prediction
    elif goal_name and completion is not None and created_date: 
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"The user has a goal: '{goal_name}'. "
                f"They are {completion}% complete, and started on {created_date}. "
                f"Estimate when they might finish this goal and give motivational advice. "
                f"Return JSON with keys: 'expectedFinishDate', 'confidence', and 'advice'."
            )

            response = model.generate_content(prompt)

            if response.candidates and response.candidates[0].content.parts:
                analysis_text = response.candidates[0].content.parts[0].text
                import json
                try:
                    # Parse AI JSON string
                    analysis_json = json.loads(analysis_text)
                except json.JSONDecodeError:
                    # Fallback if AI didn’t return valid JSON
                    analysis_json = {"expectedFinishDate": None, "confidence": 0, "advice": analysis_text}
            else:
                analysis_json = {"expectedFinishDate": None, "confidence": 0, "advice": "No prediction generated."}

            # Return parsed JSON directly
            return jsonify(analysis_json)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"prediction": "Insufficient or invalid data for prediction"}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
