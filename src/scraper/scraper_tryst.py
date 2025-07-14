# src/scraper_tryst.py

from playwright.sync_api import sync_playwright, TimeoutError, Error
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random

BASE_URL = "https://tryst.link"

URL_TEMPLATE = (
    "https://tryst.link/search?"
    "loc=-37.814%2C144.96332%3AMelbourne%2C+Victoria%2C+Australia"
    "&within=100km&trans={trans}&gender%5B%5D={gender}&q=&page={page}"
)

def scrape_profiles(gender="trans", max_pages=20):
    all_data = []

    with sync_playwright() as p:
        for page_num in range(1, max_pages + 1):
            trans_flag = "true" if gender == "trans" else "false"
            search_url = URL_TEMPLATE.format(trans=trans_flag, gender=gender, page=page_num)
            print(f"\n🔎 Navigating to {search_url}")

            try:
                browser = p.chromium.launch(headless=False, slow_mo=random.randint(800, 1600))
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                page = context.new_page()

                page.goto(search_url, timeout=30000)
                time.sleep(random.uniform(6, 10))

                try:
                    page.wait_for_selector("a.d-flex.wide-thumb", timeout=10000)
                except TimeoutError:
                    print("🔒 CAPTCHA or no listings. Solve CAPTCHA and press ENTER...")
                    input("Press ENTER once ready...")
                    page.wait_for_selector("a.d-flex.wide-thumb", timeout=15000)

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                cards = soup.select("a.d-flex.wide-thumb")
                print(f"📄 Page {page_num}: Found {len(cards)} cards")

                if not cards:
                    print("🚫 No more profiles found. Stopping.")
                    browser.close()
                    break

                for card in cards:
                    try:
                        link = BASE_URL + card["href"]
                        name_tag = card.select_one("h2.font-size-base")
                        desc_tag = card.select_one("p.font-size-small")

                        name = name_tag.text.strip() if name_tag else "N/A"
                        description = desc_tag.text.strip() if desc_tag else "N/A"

                        all_data.append({
                            "name": name,
                            "description": description,
                            "profile_url": link,
                            "category": gender
                        })
                    except Exception as e:
                        print(f"❌ Error parsing a card: {e}")
                        continue

                browser.close()
                time.sleep(random.uniform(12, 20))

            except (TimeoutError, Error) as e:
                print(f"⚠️ Failed to load page {page_num}: {e}")
                try:
                    browser.close()
                except:
                    pass
                break

    df = pd.DataFrame(all_data)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    for gender in ["trans", "female", "male", "non-binary"]:
        print(f"\n🌍 Scraping gender: {gender}")
        df = scrape_profiles(gender=gender, max_pages=20)
        filename = f"data/tryst_{gender}_melbourne.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Scraped {len(df)} profiles and saved to {filename}")
