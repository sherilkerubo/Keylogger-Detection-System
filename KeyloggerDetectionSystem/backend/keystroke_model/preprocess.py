

import os
import pandas as pd
import numpy as np

# Load original DSL dataset
df = pd.read_csv(r"C:/Users/HP/Documents/FOURTH YEAR PROJECT/KeyloggerDetectionSystem/backend/keystroke_model/DSL-StrongPasswordData.csv")

# Drop metadata columns
df = df.drop(columns=["subject", "sessionIndex", "rep"])

# Label real human data as benign (0)
df["label"] = 0
normal_data = df.copy()

# Create synthetic malicious samples
anomaly_data = normal_data.copy()
timing_cols = [col for col in anomaly_data.columns if col != "label"]
anomaly_data[timing_cols] = anomaly_data[timing_cols] * np.random.uniform(1.5, 2.5)
anomaly_data["label"] = 1

# Combine and shuffle
combined_df = pd.concat([normal_data, anomaly_data], ignore_index=True)
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# ✅ Ensure directory exists
output_dir = "keystroke_model"
os.makedirs(output_dir, exist_ok=True)

# 🔁 Save the file
combined_df.to_csv(os.path.join(output_dir, "keystroke_dataset_labeled.csv"), index=False)
print("✅ Labeled dataset saved.")
