from flask import Flask, request, jsonify
from flasgger import Swagger
import joblib
import pandas as pd
from pathlib import Path

app = Flask(__name__)
swagger = Swagger(app)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

model = joblib.load(MODEL_PATH)

REQUIRED_COLUMNS = [
    "Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation",
    "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm",
    "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm",
    "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm",
    "Temp9am", "Temp3pm", "RainToday"
]

@app.route("/")
def home():
    return jsonify({
        "message": "Rainfall Prediction API is running",
        "swagger": "/apidocs"
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict rainfall for tomorrow
    ---
    tags:
      - Prediction
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            Date: {type: string, example: "2008-12-01"}
            Location: {type: string, example: "Albury"}
            MinTemp: {type: number, example: 13.4}
            MaxTemp: {type: number, example: 22.9}
            Rainfall: {type: number, example: 0.6}
            Evaporation: {type: number, example: 4.0}
            Sunshine: {type: number, example: 9.0}
            WindGustDir: {type: string, example: "W"}
            WindGustSpeed: {type: number, example: 44}
            WindDir9am: {type: string, example: "W"}
            WindDir3pm: {type: string, example: "WNW"}
            WindSpeed9am: {type: number, example: 20}
            WindSpeed3pm: {type: number, example: 24}
            Humidity9am: {type: number, example: 71}
            Humidity3pm: {type: number, example: 22}
            Pressure9am: {type: number, example: 1007.7}
            Pressure3pm: {type: number, example: 1007.1}
            Cloud9am: {type: number, example: 8}
            Cloud3pm: {type: number, example: 7}
            Temp9am: {type: number, example: 16.9}
            Temp3pm: {type: number, example: 21.8}
            RainToday: {type: string, example: "No"}
    responses:
      200:
        description: Prediction result
      400:
        description: Bad request
      500:
        description: Server error
    """
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Invalid JSON body"}), 400

        missing = [col for col in REQUIRED_COLUMNS if col not in data]
        if missing:
            return jsonify({"error": f"Missing columns: {missing}"}), 400

        df = pd.DataFrame([data])

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1] if hasattr(model, "predict_proba") else None

        return jsonify({
            "prediction": "Yes" if int(pred) == 1 else "No",
            "probability_rain": float(prob) if prob is not None else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
