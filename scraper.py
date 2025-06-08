import time
import requests
from bs4 import BeautifulSoup
import random

# SEARCH_URL = "https://www.kleinanzeigen.de/s-anzeige:angebote/fusion-ticket/k0"
SEARCH_URL = "https://www.kleinanzeigen.de/s-zu-verschenken/c192"
INTERVAL = (5, 10)
SEEN_FILE = "seen_ads.txt"

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_seen(ad_id):
    with open(SEEN_FILE, "a") as f:
        f.write(ad_id + "\n")

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

            # if "fusion" in title.lower():   FILTER WIRD DURCH KLEINANZEIGEN SUCHFILTER NICHT BENOETIGT
            found.append((ad_id, f"https://www.kleinanzeigen.de{link}", title))
        except Exception as e:
            print(f"⚠️ Fehler beim Verarbeiten einer Anzeige: {e}")
    return found

def main():
    seen = load_seen()
    print("👀 Starte Suche nach neuen Fusion-Tickets...")

    while True:
        ads = get_ads()
        for ad_id, url, title in ads:
            if ad_id not in seen:
                print(f"[{time.strftime('%H:%M:%S')}] ✨ Neue Anzeige: {title} → {url}")
                save_seen(ad_id)
                seen.add(ad_id)
                try:
                    print(f"🚀 (TEST) Würde jetzt Nachricht auslösen für: {url}")
                except Exception as e:
                    print(f"🚨 Fehler beim Nachrichtensimulation: {e}")
                # try:
                #     res = requests.post("http://localhost:5000/send", json={"url": url}, timeout=5)
                #     if res.status_code != 200:
                #         print(f"❌ Fehler beim Aufruf des Messengers: {res.status_code} – {res.text}")
                # except requests.RequestException as e:
                #     print(f"🚨 API-Verbindungsfehler: {e}")
        time.sleep(random.uniform(*INTERVAL))

if __name__ == "__main__":
    main()