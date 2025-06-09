import time
import requests
from bs4 import BeautifulSoup
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Config
SEARCH_URL = os.getenv("SEARCH_URL")
if not SEARCH_URL or not SEARCH_URL.startswith("http"):
    print("❌ SEARCH_URL is missing or invalid. Please check your .env file.")
    exit(1)

BLACKLIST_RAW = os.getenv("BLACKLIST", "")
BLACKLIST = [word.strip().lower()
             for word in BLACKLIST_RAW.split(",") if word.strip()]

INTERVAL = (5, 10)  # seconds
SEEN_FILE = "seen_ads.txt"
IGNORED_FILE = "ignored_ads.txt"

# Utility functions


def load_ids(filename):
    try:
        with open(filename, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()


def save_id(filename, ad_id):
    with open(filename, "a") as f:
        f.write(ad_id + "\n")

# Scrape search results for ads


def get_ads():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    ads = soup.select("article.aditem")
    found = []

    for ad in ads:
        try:
            ad_id = ad.get("data-adid")
            if not ad_id:
                continue  # Skip ads with missing ID

            link_tag = ad.select_one("a")
            title_tag = ad.select_one(".text-module-begin")
            if not link_tag or not title_tag:
                continue

            link = link_tag.get("href")
            title = title_tag.get_text(strip=True)
            title_lc = title.lower()

            if any(bad_word in title_lc for bad_word in BLACKLIST):
                if ad_id not in ignored:
                    print(f"Ignored due to blacklist: {title}")
                    save_id(IGNORED_FILE, ad_id)
                    ignored.add(ad_id)
                continue

            found.append((ad_id, f"https://www.kleinanzeigen.de{link}", title))
        except Exception as e:
            print(f"Error processing ad: {e}")
    return found

# Main loop


def main():
    global seen, ignored
    seen = load_ids(SEEN_FILE)
    ignored = load_ids(IGNORED_FILE)

    print("🔎 Search started...")

    while True:
        ads = get_ads()
        for ad_id, url, title in ads:
            if ad_id in seen or ad_id in ignored:
                continue

            print(f"[{time.strftime('%H:%M:%S')}] New ad found: {title} → {url}")
            save_id(SEEN_FILE, ad_id)
            seen.add(ad_id)

            try:
                res = requests.post(
                    "http://127.0.0.1:5000/send", json={"url": url}, timeout=5)
                if res.status_code != 200:
                    print(
                        f"❌ Messenger call failed: {res.status_code} – {res.text}")
            except requests.RequestException as e:
                print(f"❌ API connection error: {e}")

        time.sleep(random.uniform(*INTERVAL))


if __name__ == "__main__":
    main()
