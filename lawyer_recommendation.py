import pandas as pd
import numpy as np

# Load
df = pd.read_csv('lawyer_recommendation_csv (1).csv')

# Fill NaN in language columns with empty string
df[['lang1','lang2','lang3']] = df[['lang1','lang2','lang3']].fillna('')

# Ensure no whitespace issues
df['lang1'] = df['lang1'].str.strip()
df['lang2'] = df['lang2'].str.strip()
df['lang3'] = df['lang3'].str.strip()

# Save cleaned
df.to_csv('lawyer_dataset_cleaned.csv', index=False)
print("✅ Cleaned and saved.")