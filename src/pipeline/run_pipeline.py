import os
import pandas as pd
from cleaner import clean_file

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

all_cleaned = []

for file in os.listdir(RAW_DIR):
    if not file.endswith(".csv"):
        continue

    source = file.replace(".csv", "")
    path = os.path.join(RAW_DIR, file)

    print(f"🔍 Cleaning: {file}")
    cleaned_df = clean_file(path, source)

    if cleaned_df is not None:
        cleaned_path = os.path.join(PROCESSED_DIR, f"cleaned_{source}.csv")
        cleaned_df.to_csv(cleaned_path, index=False)
        all_cleaned.append(cleaned_df)
        print(f"✅ Saved: {cleaned_path}")
    else:
        print(f"⚠️ No data extracted from {file}")

# Merge all
if all_cleaned:
    merged = pd.concat(all_cleaned, ignore_index=True)
    merged_path = os.path.join(PROCESSED_DIR, "all_profiles.csv")
    merged.to_csv(merged_path, index=False)
    print(f"\n🎉 Merged dataset saved: {merged_path}")
else:
    print("❌ No valid data found to merge.")
