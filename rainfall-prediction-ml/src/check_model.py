import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

print("Trying to load:", MODEL_PATH)
print("Exists ?", MODEL_PATH.exists())

model = joblib.load(MODEL_PATH)
print("Model loaded successfully")
print(type(model))
