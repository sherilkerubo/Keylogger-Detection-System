import pandas as pd
import numpy as np
import os

# Load datasets (✅ correct filenames)
free_df = pd.read_csv("keystroke_model/keyrecs_model/free-text.csv")
fixed_df = pd.read_csv("keystroke_model/keyrecs_model/fixed-text.csv")

# Optional: Check structure
print("✅ Free-text columns:", free_df.columns.tolist())
print("✅ Fixed-text columns:", fixed_df.columns.tolist())

def preprocess(df, label):
    df = df.copy()
    df = df.dropna()
    df['label'] = label
    return df

# Preprocess both
normal_df = preprocess(free_df, label=0)    # Normal behavior
malicious_df = preprocess(fixed_df, label=1)  # Simulated malicious

# Exaggerate malicious timings (simulate attack behavior)
for col in malicious_df.columns:
    if "DU" in col or "DD" in col or "UD" in col or "UU" in col or "time" in col:
        malicious_df[col] = malicious_df[col] * np.random.uniform(1.2, 2.0)

# Combine and shuffle
combined_df = pd.concat([normal_df, malicious_df], ignore_index=True)
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save combined dataset
os.makedirs("keystroke_model/keyrecs_model", exist_ok=True)
combined_df.to_csv("keystroke_model/keyrecs_model/keyrecs_combined.csv", index=False)

print("✅ Preprocessed dataset saved to keyrecs_combined.csv")
