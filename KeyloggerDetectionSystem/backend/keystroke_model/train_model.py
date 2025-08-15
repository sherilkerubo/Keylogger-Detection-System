import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the labeled dataset
df = pd.read_csv("keystroke_model/keystroke_dataset_labeled.csv")

# Split into features and labels
X = df.drop(columns=["label"])
print("Training features shape:", X.shape)
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("🔍 Classification Report:\n", classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# Save the model
model_path = "keystroke_model/keystroke_model.joblib"
joblib.dump(clf, model_path)
print(f" Model saved to {model_path}")

