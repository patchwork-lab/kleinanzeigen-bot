import sys
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Lade Zugangsdaten aus .env (optional, falls Login notwendig)
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Nachricht, die versendet werden soll
MESSAGE_TEXT = os.getenv("MESSAGE_TEXT")

if not MESSAGE_TEXT:
    print("MESSAGE_TEXT in .env fehlt!")
    sys.exit(1)


def setup_driver():
    options = uc.ChromeOptions()
    PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH")

    if not PROFILE_PATH or not os.path.exists(PROFILE_PATH):
        print(
            f"❌ CHROME_PROFILE_PATH in .env fehlt oder ist ungültig: {PROFILE_PATH}")
        sys.exit(1)

    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")
    options.headless = False  # Debug sichtbar
    return uc.Chrome(options=options)


def is_logged_in(driver):
    driver.get("https://www.kleinanzeigen.de/m-meine-anzeigen.html")
    time.sleep(3)
    return "Meine Anzeigen" in driver.title or "anzeigen" in driver.page_source.lower()


def send_message(driver, url):
    print(f"🔗 Öffne Anzeige: {url}")
    driver.get(url)
    time.sleep(5)

    try:
        # Nachricht schreiben
        textarea = driver.find_element(By.NAME, "message")
        textarea.clear()
        textarea.send_keys(MESSAGE_TEXT)
        time.sleep(1)

        # Neuer Button: Klasse statt veraltetes data-testid
        send_button = driver.find_element(
            By.CSS_SELECTOR, "button.viewad-contact-submit")
        driver.execute_script("arguments[0].click();", send_button)
        time.sleep(4)

        print(f"✅ Nachricht wurde abgeschickt an: {url}")
    except Exception as e:
        print(f"❌ Fehler beim Nachrichtensenden: {e}")


def main(url):
    driver = setup_driver()
    time.sleep(2)

    if not is_logged_in(driver):
        print("⚠️ Nicht eingeloggt. Bitte manuell einloggen.")
        input("⏸ Logge dich im geöffneten Chrome ein und drücke [Enter]...")
        if not is_logged_in(driver):
            print("❌ Login nicht erkannt. Beende.")
            driver.quit()
            return

    send_message(driver, url)
    input(
        "\n⏸ Vorgang abgeschlossen. Drücke [Enter], um Chrome zu schließen...")
    driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Verwendung: python messenger.py <anzeige-url>")
        sys.exit(1)
    main(sys.argv[1])
