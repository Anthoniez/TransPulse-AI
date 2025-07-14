import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# === Paths ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
input_path = os.path.join(BASE_DIR, "data", "processed", "all_profiles.csv")
output_path = os.path.join(BASE_DIR, "data", "enriched", "all_profiles_topics.csv")

# === Load Data ===
df = pd.read_csv(input_path)
df["description"] = df["description"].fillna("")

# === TF-IDF Vectorization ===
tfidf = TfidfVectorizer(
    max_df=0.9,      # Ignore very common words
    min_df=5,        # Ignore very rare words
    stop_words="english",
    max_features=1000
)
X = tfidf.fit_transform(df["description"])

# === Topic Modeling with NMF ===
n_topics = 6
nmf = NMF(n_components=n_topics, random_state=42)
topic_matrix = nmf.fit_transform(X)

# === Top Words per Topic ===
feature_names = tfidf.get_feature_names_out()
topics = []
for topic_idx, topic in enumerate(nmf.components_):
    top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
    topics.append(", ".join(top_words))
    print(f"🧠 Topic {topic_idx + 1}: {', '.join(top_words)}")

# === Assign Dominant Topic to Each Description ===
df["topic_id"] = topic_matrix.argmax(axis=1)
df["topic_keywords"] = df["topic_id"].apply(lambda x: topics[x])

# === Save Results ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"✅ Topic modeling complete. Saved to: {output_path}")
