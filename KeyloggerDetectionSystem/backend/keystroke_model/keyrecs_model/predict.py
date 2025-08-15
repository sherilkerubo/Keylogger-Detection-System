import os
import joblib

# Load model
model_path = os.path.join(os.path.dirname(__file__), "keyrecs_model.joblib")
clf = joblib.load(model_path)

# Predict using the 81-feature model
def is_keyrecs_malicious(features: list) -> bool:
    prediction = clf.predict([features])[0]
    return prediction == 1
