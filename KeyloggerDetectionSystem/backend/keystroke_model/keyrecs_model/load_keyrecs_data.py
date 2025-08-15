import pandas as pd
import os

# Load the fixed-text dataset
df = pd.read_csv("keystroke_model/keyrecs_model/free-text.csv")
# Print columns for confirmation
print(df.columns.tolist())

# Label: even IDs = normal (0), odd = malicious (1)
df['label'] = df['participant'].apply(lambda x: int(x[1:]) % 2)

# Drop participant column
df = df.drop(columns=['participant'], errors='ignore')

# ... after labeling and cleaning your dataframe
output_path = os.path.join(os.path.dirname(__file__), "keystroke_dataset_labeled.csv")
df.to_csv(output_path, index=False)
print(f"✅ Saved labeled dataset to {output_path}")



