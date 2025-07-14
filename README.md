# TransPulse AI

**TransPulse AI** is an intelligent data pipeline designed to extract, clean, and analyze classified escort ads from platforms such as Tryst and Locanto. Built with a combination of web scraping, natural language processing (NLP), and clustering algorithms, it transforms messy, unstructured data into actionable market insights.

> This project is part of my data science portfolio and showcases advanced scraping techniques, NLP pipelines, and unsupervised machine learning for text classification and similarity detection.

# What Inspired This Project?

ITransPulse AI was inspired by a real-world opportunity: an adult entertainment agency approached me seeking data-driven insights into their market — including trends, competitor positioning, and customer preferences.

Unlike traditional industries, this sector has very little structured data. Service listings are scattered across classified platforms, written in free-form text, and change frequently. This posed a unique technical challenge:
How can we extract intelligence from dynamic, messy, and unstructured data?

**TransPulse AI was born out of that challenge:**

To scrape dynamic, real-world data at scale
To clean and structure raw, messy content
And most importantly, to apply NLP techniques like Named Entity Recognition and topic modeling.
To reveal patterns, trends, and insights that agencies could use to optimize operations, pricing, marketing, and hiring

I wanted to turn noise into signals, using tools like spaCy, topic modeling, and clustering to build not just a dataset — but a lens into an underground, data-rich world that rarely gets analyzed.

**This project reflects my passion for:**

Using AI to solve unconventional real-world problems

Building automated data pipelines that turn chaos into clarity

And applying machine learning in domains that are overlooked or underserved

## The adult industry may be unconventional, but it is also data-rich and insight-poor — and that made it the perfect challenge for an applied AI project.

## Features

- **Web Scraping**

  - Automated scraping of escort and massage ads from dynamic platforms using Playwright.
  - Handles pagination, content extraction, and basic CAPTCHA detection.
  - HTML snapshots and debug logs for scraper reliability.

- **Data Structuring**

  - Raw HTML is parsed and converted into structured CSV/JSON datasets.
  - Profile metadata, service descriptions, and location data extracted.

- **NLP & Enrichment**

  - Text preprocessing: cleaning, lemmatization, and vectorization.
  - Named Entity Recognition (NER) with spaCy.
  - Topic modeling using TF-IDF + NMF.
  - Sentiment analysis and clone/similarity detection.

- **Modular Pipeline**

  - Scripts organized into stages: `scraping`, `cleaning`, `enriching`, `modeling`.
  - Easily extendable with new sources or ML models.

- **Visualization**
  - Notebooks for data exploration and topic insights.
  - Optional Streamlit UI (in progress).

---

## Use Cases

- Market trend analysis for escort services
- NLP experimentation on unstructured classified data
- Clustering and similarity scoring of service descriptions
- Prototype for service directory intelligence (beyond adult sector)

---

## Project Structure

├── .gitignore
├── README.md
├── app
├── data
│ ├── enriched
│ ├── exports
│ │ ├── .keep
│ ├── features
│ │ └── .keep
│ ├── logs
│ │ ├── .keep
│ │ └── cleaning_errors.log
│ ├── processed
│ │ ├── .keep
│ └── raw
│ ├── .keep
├── debug_tryst_page.html
├── generate_tree.py
├── models
├── notebooks
│ ├── eda_profiles.ipynb
│ ├── eda_profiles_plotly.ipynb
│ ├── nlp_clustering.ipynb
│ ├── nlp_entities.ipynb
│ ├── outputs
│ │ ├── age_distribution.html
│ │ ├── category_counts.html
│ │ ├── desc_length_by_category.html
│ │ ├── escort_clusters.html
│ │ ├── top_20_locations.html
│ │ └── top_reused_phones.html
│ └── topic_modeling.ipynb
├── project_structure.txt
├── project_tree.txt
├── requirements.txt
├── src
│ ├── pipeline
│ │ ├── cleaner.py
│ │ ├── enrich
│ │ │ ├── nlp_entities.py
│ │ │ └── topic_modeling.py
│ │ ├── run_pipeline.py
│ │ └── storage.py
│ └── scraper
│ ├── scraper_escortify.py
│ ├── scraper_locanto.py
│ ├── scraper_tryst.py
│ └── trigger.py
└── tryst_screenshot.png

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/TransPulse-AI.git
cd TransPulse-AI

```

2. **Set up the virtual environment**

python3 -m venv transpulse
source transpulse/bin/activate

3. **Install Code Dependencies**
   pip install -r requirements.txt

4. **Download spaCy model(if version issue occures)**
   python -m spacy download en_core_web_sm

## Usage

1. **Run the Scrapers**
   python src/scraping/tryst_scraper.py

2. **Run NLP enrichment**

python src/enrich/nlp_entities.py

3. **Explore insights in Jupyter**

jupyter notebook notebooks/analysis.ipynb

## Requirements

Python 3.8+
Playwright
BeautifulSoup
spaCy
scikit-learn
pandas
numpy
matplotlib / seaborn (optional)

## Disclaimer

This project is for educational and research purposes only. No scraped data is published or distributed. The focus is on developing NLP and data engineering pipelines using publicly available content. Please respect platform terms of service

## Author

Anthoniez Fernando
Data Science and AI Automation Enthusiast
Passionate about NLP, web scraping, and building intelligent data pipelines.
🔗 LinkedIn : https://www.linkedin.com/in/jayamini-anthoniez-fernando/
📧 Contact Me : jayfernandojay@gmail.com
