import pandas as pd
import numpy as np
# Load the dataset
df = pd.read_csv("C:/Users/HP/Documents/FOURTH YEAR PROJECT/KeyloggerDetectionSystem/backend/keystroke_model/DSL-StrongPasswordData.csv")  # Replace with your actual path

# Display general info and first few rows
print(df.info())
print(df.head())


# Load your dataset
df = pd.read_csv(r"C:/Users/HP/Documents/FOURTH YEAR PROJECT/KeyloggerDetectionSystem/backend/keystroke_model/DSL-StrongPasswordData.csv")

# Drop metadata columns
df = df.drop(columns=["subject", "sessionIndex", "rep"])

# Label this real data as benign (normal)
df["label"] = 0

# 👨 Normal data = keystroke timings
normal_data = df.copy()

# 👹 Generate synthetic malicious data
# Method: scale timings to simulate keylogger injection (e.g., delay / anomalies)
anomaly_data = normal_data.copy()
timing_cols = [col for col in anomaly_data.columns if col != "label"]
anomaly_data[timing_cols] = anomaly_data[timing_cols] * np.random.uniform(1.5, 2.5)  # Add timing anomaly
anomaly_data["label"] = 1  # Mark as malicious

# ✅ Combine both datasets
combined_df = pd.concat([normal_data, anomaly_data], ignore_index=True)

# ✅ Shuffle the data
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# 🔁 Save the preprocessed data
combined_df.to_csv("keystroke_model/keystroke_dataset_labeled.csv", index=False)
print("✅ Labeled dataset saved.")
