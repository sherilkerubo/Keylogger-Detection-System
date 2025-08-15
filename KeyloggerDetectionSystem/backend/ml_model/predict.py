
import joblib
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None


def is_malicious(features):
    if not model:
        return False  # fallback if model not found
    try:
        features_np = np.array(features).reshape(1, -1)
        prediction = model.predict(features_np)
        return bool(prediction[0])
    except Exception:
        return False