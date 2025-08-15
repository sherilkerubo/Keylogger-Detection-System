# backend/keystroke_model/predict.py
import joblib
import numpy as np
import os
from joblib import load

# ✅ Load KeyRecs model
# ✅ Correct
model_path = os.path.join(os.path.dirname(__file__), "keystroke_model.joblib")

clf = joblib.load(model_path)

# ✅ Prediction function
def is_keystroke_malicious(features: list) -> bool:
    prediction = clf.predict([features])[0]
    return prediction == 1


#Set threshold 
CONFIDENCE_THRESHOLD = 0.80

def is_keystroke_malicious(features):
    if not isinstance(features, (list, np.ndarray)):
        raise ValueError("Expected features as list or numpy array")

    proba = clf.predict_proba([features])[0]
    predicted_label = clf.classes_[np.argmax(proba)]
    confidence = np.max(proba)

    print(f"[Prediction] Label: {predicted_label}, Confidence: {confidence:.4f}")

    if predicted_label == 1 and confidence >= CONFIDENCE_THRESHOLD:
        return True
    return False




