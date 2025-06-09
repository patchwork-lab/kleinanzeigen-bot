import time
import requests
from bs4 import BeautifulSoup
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load and validate environment configuration
SEARCH_URL = os.getenv("SEARCH_URL")
if not SEARCH_URL or not SEARCH_URL.startswith("http"):
    print("❌ SEARCH_URL is missing or invalid. Please check your .env file.")
    exit(1)

BLACKLIST_RAW = os.getenv("BLACKLIST", "")
if not BLACKLIST_RAW:
    print("⚠️ BLACKLIST is not set. No keywords will be filtered.")
BLACKLIST = [word.strip().lower()
             for word in BLACKLIST_RAW.split(",") if word.strip()]

INTERVAL = (5, 10)  # Delay between requests in seconds (min, max)
SEEN_FILE = "seen_ads.txt"
IGNORED_FILE = "ignored_ads.txt"  # Optional: Track ignored ads for debugging

# Load already seen ad IDs


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

# Save a seen ad ID


def save_seen(ad_id):
    with open(SEEN_FILE, "a") as f:
        f.write(ad_id + "\n")

# Save an ignored ad ID (optional, not used in matching)


def save_ignored(ad_id):
    with open(IGNORED_FILE, "a") as f:
        f.write(ad_id + "\n")

# Scrape the search results for ads


def get_ads():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    ads = soup.select("article.aditem")
    found = []

    for ad in ads:
        try:
            ad_id = ad.get("data-adid")
            link_tag = ad.select_one("a")
            title_tag = ad.select_one(".text-module-begin")
            if not ad_id or not link_tag or not title_tag:
                continue

            link = link_tag.get("href")
            title = title_tag.get_text(strip=True)
            title_lc = title.lower()

            if any(bad_word in title_lc for bad_word in BLACKLIST):
                print(f"Ignored due to blacklist: {title}")
                save_ignored(ad_id)
                continue

            found.append((ad_id, f"https://www.kleinanzeigen.de{link}", title))
        except Exception as e:
            print(f"Error processing ad: {e}")
    return found

# Main loop: continuously check for new ads


def main():
    seen = load_seen()
    print("🔎 Search started...")

    while True:
        ads = get_ads()
        for ad_id, url, title in ads:
            if ad_id not in seen:
                print(
                    f"[{time.strftime('%H:%M:%S')}] New ad found: {title} → {url}")
                save_seen(ad_id)
                seen.add(ad_id)
                try:
                    res = requests.post(
                        "http://127.0.0.1:5000/send", json={"url": url}, timeout=5
                    )
                    if res.status_code != 200:
                        print(
                            f"❌ Messenger call failed: {res.status_code} – {res.text}")
                except requests.RequestException as e:
                    print(f"❌ API connection error: {e}")
        time.sleep(random.uniform(*INTERVAL))


if __name__ == "__main__":
    main()
