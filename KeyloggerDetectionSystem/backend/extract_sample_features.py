import pandas as pd

# STEP 1: Load dataset
csv_path = csv_path = "C:\\Users\\HP\\Documents\\FOURTH YEAR PROJECT\\Keylogger_Detection_Dataset.csv"
 # 🔁 Replace with the actual path
df = pd.read_csv(csv_path)

# STEP 2: Drop non-numeric columns and label
drop_cols = ['Flow ID', ' Source IP', ' Destination IP', ' Timestamp', 'Class']
df_clean = df.drop(columns=drop_cols, errors='ignore')

# STEP 3: Drop rows with missing values
df_clean = df_clean.dropna()

# STEP 4: Pick first row with exactly 81 features
if df_clean.shape[1] != 81:
    print(f"⚠️ WARNING: Dataset has {df_clean.shape[1]} features instead of 81")
else:
    sample = df_clean.iloc[0].tolist()
    print("✅ Extracted 81-feature vector:")
    print(sample)
    print(f"\n🧮 Length: {len(sample)}")
