import pandas as pd
import re

STANDARD_COLUMNS = [
    "title", "description", "profile_url", "phone", "age",
    "location", "image_url", "category", "source"
]

def extract_phone(text):
    match = re.findall(r'\b\d{4}[\s]?\d{3}[\s]?\d{3}\b', str(text))
    return match[0] if match else ""

def extract_age_structured(text):
    match = re.search(r'\b(\d{2})\s?years?', str(text), re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_age_nlp(text):
    text = str(text).lower()
    match = re.search(r'\b(1[89]|[2-5][0-9]|60)\s?(yo|years|yrs|year[- ]old)?\b', text)
    return int(match.group(1)) if match else None

def clean_file(filepath, source):
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

    cleaned = pd.DataFrame(columns=STANDARD_COLUMNS)
    cleaned["source"] = source

    if "Profile URL" in df.columns:  # Escortify format
        cleaned["title"] = df["Name"]
        cleaned["description"] = df["Description"]
        cleaned["profile_url"] = df["Profile URL"].str.replace(
            "https://escortify.com.auhttps://escortify.com.au",
            "https://escortify.com.au",
            regex=False
        )
        cleaned["phone"] = df["Phone"].apply(extract_phone)
        # Combine age from 'Age' and description
        cleaned["age"] = df["Age"].apply(extract_age_structured).combine_first(df["Description"].apply(extract_age_nlp))
        cleaned["location"] = df["Location"]
        cleaned["image_url"] = df["Image URL"]
        cleaned["category"] = df["Type"].astype(str).str.strip()

    elif "profile_url" in df.columns:  # Locanto / Tryst
        cleaned["title"] = df["name"]
        cleaned["description"] = df["description"]
        cleaned["profile_url"] = df["profile_url"]
        cleaned["phone"] = df["description"].apply(extract_phone)
        cleaned["age"] = df["description"].apply(extract_age_nlp)
        cleaned["location"] = df["description"].str.extract(
            r"(?i)(melbourne|brisbane|sydney|perth|adelaide|canberra|hobart|darwin)"
        )
        cleaned["image_url"] = ""
        cleaned["category"] = df["category"]

    else:
        print(f"⚠️ Skipped unknown format: {filepath}")
        return None

    cleaned = cleaned.drop_duplicates(subset=["profile_url"])
    cleaned = cleaned.dropna(subset=["profile_url", "title"])
    cleaned = cleaned.fillna("")
    return cleaned
