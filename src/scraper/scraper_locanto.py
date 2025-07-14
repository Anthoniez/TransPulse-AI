# src/scraper_locanto.py

from playwright.sync_api import sync_playwright, TimeoutError, Error
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random

URLS = {
    "femaleEscort": [
        "https://www.locanto.com.au/melbourne/Escorts/20905/?query=&dist=150",
        "https://www.locanto.com.au/melbourne/Women-Looking-for-Men/20702/?query=&dist=150"
    ],
    "transEscort": [
        "https://www.locanto.com.au/melbourne/T4m/20960/?query=&dist=150",
        "https://www.locanto.com.au/melbourne/Transgender-Adventures/20711/?query=&dist=150"
    ],
    "massage": [
        "https://www.locanto.com.au/melbourne/Massages/20901/?dist=150"
    ],
    "maleEscort": [
        "https://www.locanto.com.au/melbourne/M4m/20968/?query=&dist=150"
    ],
    "jobs": [
        "https://www.locanto.com.au/melbourne/Exotic-Dancers/20952/?query=&dist=150",
        "https://www.locanto.com.au/geo/502976/Jobs/20954/Clayton-North/?dist=150",
        "https://www.locanto.com.au/geo/502976/Erotic-Photographers-Models/20964/Clayton-North/?dist=150"
    ]
}

PAGES = 3

def scrape_locanto_profiles(label="femaleEscort", max_pages=PAGES):
    all_data = []
    urls = URLS.get(label, [])

    with sync_playwright() as p:
        for base_url in urls:
            for page_num in range(1, max_pages + 1):
                url = f"{base_url}&page={page_num}" if page_num > 1 else base_url
                print(f"\n🌆 Scraping {label.upper()} — Page {page_num}")
                print(f"🔎 URL: {url}")

                try:
                    browser = p.chromium.launch(headless=False, slow_mo=random.randint(1000, 2000))
                    context = browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                    )
                    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    page = context.new_page()

                    page.goto(url, timeout=45000)
                    time.sleep(random.uniform(8, 12))

                    try:
                        page.wait_for_selector("article.posting_listing", timeout=10000)
                    except TimeoutError:
                        print("🔒 CAPTCHA or no listings. Solve CAPTCHA and press ENTER...")
                        input("Press ENTER once ready...")
                        page.wait_for_selector("article.posting_listing", timeout=15000)

                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    cards = soup.select("article.posting_listing")
                    print(f"📄 Found {len(cards)} cards")

                    if not cards:
                        print("🚫 No cards found. Stopping early.")
                        browser.close()
                        break

                    for card in cards:
                        try:
                            a_tag = card.find("a", class_="js-ad_link")
                            name_tag = card.select_one("div.h3.js-result_title")
                            desc_tag = card.select_one("div.posting_listing__description")

                            name = name_tag.text.strip() if name_tag else "N/A"
                            description = desc_tag.text.strip() if desc_tag else "N/A"
                            profile_url = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""

                            all_data.append({
                                "name": name,
                                "description": description,
                                "profile_url": profile_url,
                                "category": label
                            })
                        except Exception as e:
                            print(f"❌ Error parsing card: {e}")

                    browser.close()
                    time.sleep(random.uniform(15, 25))

                except (TimeoutError, Error) as e:
                    print(f"⚠️ Failed to load page: {e}")
                    try:
                        browser.close()
                    except:
                        pass

    df = pd.DataFrame(all_data)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    for category in URLS.keys():
        df = scrape_locanto_profiles(label=category, max_pages=PAGES)
        file_path = f"data/locanto_{category}.csv"
        df.to_csv(file_path, index=False)
        print(f"\n✅ Scraped {len(df)} {category} profiles. Saved to {file_path}")