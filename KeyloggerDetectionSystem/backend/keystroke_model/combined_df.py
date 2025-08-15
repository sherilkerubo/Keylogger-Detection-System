import pandas as pd
import numpy as np

# Load both datasets (adjust file paths)
free_df = pd.read_csv("path/to/free-text.csv")
fixed_df = pd.read_csv("path/to/fixed-text.csv")

# --- Optional: Simulate malicious version by modifying timing features ---
malicious_df = fixed_df.copy()
for col in malicious_df.columns:
    if "latency" in col or "time" in col or "DD" in col or "UD" in col or "H." in col:
        malicious_df[col] = malicious_df[col] * np.random.uniform(1.5, 2.5)  # exaggerate timing

# --- Label the data ---
free_df["label"] = 0
fixed_df["label"] = 0
malicious_df["label"] = 1

# --- Combine into one dataset ---
combined_df = pd.concat([free_df, fixed_df, malicious_df], ignore_index=True)
combined_df = combined_df.sample(frac=1).reset_index(drop=True)  # Shuffle

print("Combined shape:", combined_df.shape)
print("Columns:", combined_df.columns.tolist())
