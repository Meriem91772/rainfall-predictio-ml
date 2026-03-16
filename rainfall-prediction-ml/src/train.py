import pandas as pd
import joblib
from pathlib import Path
import time

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "weatherAUS.csv"
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"


def load_data():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["RainTomorrow"]).copy()
    df["RainTomorrow"] = df["RainTomorrow"].map({"No": 0, "Yes": 1})

    print(f"Dataset shape after cleaning: {df.shape}")
    return df


def build_pipeline(model, X):
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = X.select_dtypes(include=["object", "string"]).columns

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    return pipeline


if __name__ == "__main__":
    start_total = time.time()

    df = load_data()

    X = df.drop("RainTomorrow", axis=1)
    y = df["RainTomorrow"]

    print("Splitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression(
        max_iter=1000,
        solver="liblinear",
        class_weight="balanced"
    )

    print("\nTraining logistic regression...")
    pipeline = build_pipeline(model, X_train)
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    print("\nModel: logreg")
    print("Accuracy:", accuracy_score(y_test, preds))
    print("F1:", f1_score(y_test, preds))
    print(classification_report(y_test, preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")

    print(f"\nTotal execution time: {time.time() - start_total:.2f} sec")
