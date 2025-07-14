# escortify_scraper.py

import asyncio
import csv
import os
from playwright.async_api import async_playwright

# Ensure output directory exists
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "escortify_melbourne.csv")

BASE_URL = "https://escortify.com.au/melbourne-escorts?page={}"

async def scrape_page(page, url):
    await page.goto(url)
    await page.wait_for_selector(".listing-detail", timeout=10000)
    listings = await page.query_selector_all(".listing-detail")
    data = []

    for listing in listings:
        try:
            title_tag = await listing.query_selector("a.listing-thumb")
            profile_url = await title_tag.get_attribute("href")
            name = await listing.query_selector("#escort-name")
            name_text = await name.inner_text() if name else ""

            image_tag = await listing.query_selector("img")
            image_url = await image_tag.get_attribute("src") if image_tag else ""

            active = await listing.query_selector(".seller_txt")
            last_active = await active.inner_text() if active else ""

            age = await listing.query_selector(".bluebubbles span")
            age_text = await age.inner_text() if age else ""

            desc = await listing.query_selector(".profile_stuff")
            desc_text = await desc.inner_text() if desc else ""

            phone_tag = await listing.query_selector(".mobilenew")
            phone = await phone_tag.inner_text() if phone_tag else ""

            location_block = await listing.query_selector(".vipphone")
            location_text = await location_block.inner_text() if location_block else ""
            location = location_text.split("|")[0].strip() if "|" in location_text else ""
            escort_type = location_text.split("|")[1].strip() if "|" in location_text else ""

            duration_tag = await listing.query_selector(".vippricenew")
            duration_text = await duration_tag.inner_text() if duration_tag else ""
            duration = duration_text.split("\n")[0].strip()

            data.append({
                "Name": name_text,
                "Profile URL": "https://escortify.com.au" + profile_url,
                "Image URL": image_url,
                "Last Active": last_active,
                "Age": age_text,
                "Description": desc_text,
                "Location": location,
                "Type": escort_type,
                "Phone": phone,
                "Duration": duration
            })
        except Exception as e:
            print(f"Error scraping listing: {e}")
            continue

    return data

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        all_data = []

        for i in range(1, 6):
            print(f"Scraping Page {i}...")
            url = BASE_URL.format(i)
            try:
                listings = await scrape_page(page, url)
                if not listings:
                    print("No listings found on this page.")
                    break
                all_data.extend(listings)
            except Exception as e:
                print(f"Failed to scrape page {i}: {e}")
                continue

        if all_data:
            with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
                writer.writeheader()
                writer.writerows(all_data)

            print(f"\n✅ Scraped {len(all_data)} profiles. Saved to {OUTPUT_CSV}")
        else:
            print("⚠️ No data to save.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
