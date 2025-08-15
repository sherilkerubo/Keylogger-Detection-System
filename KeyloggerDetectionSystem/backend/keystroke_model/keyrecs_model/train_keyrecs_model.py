import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

#  Correct path construction
csv_path = os.path.join(os.path.dirname(__file__), "keyrecs_labeled.csv")

# Load and preprocess data
df = pd.read_csv(csv_path, dtype=str)  # Load everything as string
df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric
df = df.fillna(0)  # Fill missing values

# Shuffle and sample
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
df = df.sample(n=5000, random_state=42)  # Optional: use subset for speed

# Split features and labels
X = df.drop(columns=["label"], errors="ignore")
print("Training features shape:", X.shape)

y = df["label"]

# Final check and cleanup
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)
if len(X) != len(y):
    min_len = min(len(X), len(y))
    X = X.iloc[:min_len]
    y = y.iloc[:min_len]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\n🔍 Classification Report:\n")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

#  Save model
model_path = os.path.join(os.path.dirname(__file__), "keyrecs_model.joblib")
joblib.dump(clf, model_path)
print(f" Model saved to {model_path}")
