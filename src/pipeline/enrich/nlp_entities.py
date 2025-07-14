import spacy
import pandas as pd
import re
import os

# ✅ Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# ✅ Define input/output paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
input_path = os.path.join(BASE_DIR, "data", "processed", "all_profiles.csv")
output_path = os.path.join(BASE_DIR, "data", "enriched", "all_profiles_entities.csv")

# ✅ Load cleaned data
df = pd.read_csv(input_path)
df["description"] = df["description"].fillna("")

# ✅ Entity extraction function
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "MONEY": [],
        "DATE": [],
        "TIME": [],
        "SERVICES": []
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    # Regex match for escort-related services
    services = re.findall(
        r"(massage|escort|anal|bj|GFE|PSE|kiss|incall|outcall|nuru|fetish|69|cuddle|dominatrix)",
        text, re.IGNORECASE
    )
    entities["SERVICES"].extend(set(services))

    return {k: list(set(v)) for k, v in entities.items()}

# ✅ Extract entities
entity_results = df["description"].apply(extract_entities)
entities_df = pd.json_normalize(entity_results)

# ✅ Combine and save
result_df = pd.concat([df, entities_df], axis=1)

# ✅ Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# ✅ Save the enriched dataset
result_df.to_csv(output_path, index=False)
print(f"✅ Entity extraction complete. File saved to: {output_path}")
