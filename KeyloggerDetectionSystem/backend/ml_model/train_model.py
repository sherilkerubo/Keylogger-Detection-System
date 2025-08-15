import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load CSV
df = pd.read_csv(r"C:\Users\HP\Documents\FOURTH YEAR PROJECT\Keylogger_Detection_Dataset.csv")
 # replace with your actual file

# Clean column names
df.columns = df.columns.str.strip()

# Define label column
label_col = "Class"

# Check if label column exists
if label_col not in df.columns:
    print(f"Available columns: {df.columns.tolist()}")
    raise KeyError(f"'{label_col}' column not found in dataset")

# Drop rows with missing labels
df = df.dropna(subset=[label_col])

# Drop non-numeric or irrelevant columns
non_numeric_cols = ["Flow ID", "Source IP", "Destination IP", "Timestamp"]
cols_to_drop = [col for col in non_numeric_cols if col in df.columns]
print(f"Dropping non-numeric columns: {cols_to_drop}")
df = df.drop(columns=cols_to_drop, errors='ignore')

# Separate features and labels
X = df.drop(columns=[label_col], errors='ignore')
y = df[label_col]

# Convert to numeric
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(0)

# Match lengths
if len(X) != len(y):
    print(f"Mismatch detected! len(X) = {len(X)}, len(y) = {len(y)}")
    min_len = min(len(X), len(y))
    X = X.iloc[:min_len]
    y = y.iloc[:min_len]

print("Final shapes:")
print("X:", X.shape)
print("y:", y.shape)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save model
model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
joblib.dump(clf, model_path)
print(f"Model saved to {model_path}")
