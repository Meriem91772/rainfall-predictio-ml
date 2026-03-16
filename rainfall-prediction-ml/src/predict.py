import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

model = joblib.load(MODEL_PATH)

def predict_rain(input_dict):
    df = pd.DataFrame([input_dict])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1] if hasattr(model, "predict_proba") else None

    return {
        "prediction": "Yes" if int(pred) == 1 else "No",
        "probability_rain": float(prob) if prob is not None else None
    }
