import pickle
import os
import numpy as np

# Get model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Load model once
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_milk(ph, temperature, weight):

    # Arrange input exactly same as training order
    input_data = np.array([[ph, temperature, weight]])

    prediction = model.predict(input_data)[0]

    # If classification model
    if hasattr(model, "predict_proba"):
        probability = max(model.predict_proba(input_data)[0])
    else:
        probability = 1.0

    # Map numeric label to text (adjust if needed)
    if prediction == 0:
        risk = "Fresh"
        spoilage_hours = 6
    elif prediction == 1:
        risk = "Warning"
        spoilage_hours = 3
    else:
        risk = "Spoiled"
        spoilage_hours = 1

    return {
        "risk_level": risk,
        "probability": round(float(probability), 2),
        "spoilage_hours": spoilage_hours
    }
