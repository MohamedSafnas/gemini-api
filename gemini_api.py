from flask import Flask, request, jsonify
import google.generativeai as genai
import os


from datetime import datetime, timedelta


app = Flask(__name__)

genai.configure(api_key="AIzaSyBDUyo-bQHcvndbqxy5wLUDVV6-ZrrgFUs")  # Replace with your own key

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini API is running!"

@app.route("/generate", methods=["POST"])
def generate_steps():
    try:
        data = request.get_json()
        print("📥 Received data:", data)

        goal = data.get("goal", "")
        if not goal:
            return jsonify({"error": "Goal not provided"}), 400

        print("🎯 Goal:", goal)

    
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(f"Suggest 5 step-by-step instructions to achieve this goal: {goal}")

        print("✅ Response:", response.text)

        return jsonify({"steps": response.text})

    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500
    


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Goal-based prediction inputs
    goal_name = data.get("goalName")
    completion = data.get("completionPercentage")
    created_date = data.get("createdDate")  # YYYY-MM-DD

    # Custom prediction inputs
    title = data.get("title")
    frequency = data.get("frequency")  # "daily", "weekly", "monthly"
    duration = data.get("duration")    # hours per frequency

    if title and frequency and duration:
        # Custom prediction
        # Estimate total hours needed (example fixed 300 hours)
        total_hours = 300
        if frequency.lower() == "daily":
            hours_per_week = duration * 7
        elif frequency.lower() == "weekly":
            hours_per_week = duration
        elif frequency.lower() == "monthly":
            hours_per_week = duration / 4  # approximate weeks
        else:
            return jsonify({"prediction": "Invalid frequency"}), 400

        weeks_needed = total_hours / hours_per_week
        months_needed = weeks_needed / 4
        prediction_text = (f"With {duration} hours of {frequency} practice, "
                           f"you'll master '{title}' in approximately "
                           f"{months_needed:.1f} months ({total_hours} total hours required).")
        return jsonify({"prediction": prediction_text})

    elif goal_name and completion is not None and created_date:
        # Goal-based prediction
        try:
            created = datetime.strptime(created_date, "%Y-%m-%d")
            days_since_created = (datetime.now() - created).days
            remaining_percentage = 100 - completion
            # Estimate days to finish based on progress
            estimated_days_to_finish = int(days_since_created / (completion / 100) * (remaining_percentage / 100))
            finish_date = datetime.now() + timedelta(days=estimated_days_to_finish)
            confidence = 70  # example confidence
            prediction_text = (f"Based on your {completion}% progress in {days_since_created} days, "
                               f"you'll complete '{goal_name}' on {finish_date.strftime('%B %d, %Y')} "
                               f"({confidence}% confidence). If you finish, you can achieve more advanced goals!")
            return jsonify({"prediction": prediction_text})
        except Exception as e:
            return jsonify({"prediction": f"Error: {str(e)}"}), 400

    else:
        return jsonify({"prediction": "Insufficient or invalid data for prediction"}), 400





# ✅ Run Flask on correct host and port for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
