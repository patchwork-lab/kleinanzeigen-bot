import sys
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
MESSAGE_TEXT = os.getenv("MESSAGE_TEXT")

# Exit early if no message text is provided
if not MESSAGE_TEXT:
    print("❌ MESSAGE_TEXT missing in .env!")
    sys.exit(1)


def setup_driver():
    options = uc.ChromeOptions()
    PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH")

    if not PROFILE_PATH or not os.path.exists(PROFILE_PATH):
        print(f"❌ CHROME_PROFILE_PATH missing or invalid: {PROFILE_PATH}")
        sys.exit(1)

    # Load Chrome user profile
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")
    options.headless = False  # Show browser for debugging
    return uc.Chrome(options=options)


def is_logged_in(driver):
    # Navigate to user ads page to verify login
    driver.get("https://www.kleinanzeigen.de/m-meine-anzeigen.html")
    time.sleep(2)
    return "Meine Anzeigen" in driver.title or "anzeigen" in driver.page_source.lower()


def send_message(driver, url):
    print(f"🔗 Opening listing: {url}")
    driver.get(url)
    time.sleep(3)

    try:
        # Locate message input field and enter the message
        textarea = driver.find_element(By.NAME, "message")
        textarea.clear()
        textarea.send_keys(MESSAGE_TEXT)
        time.sleep(1)

        # Locate the send button using CSS class (updated selector)
        send_button = driver.find_element(
            By.CSS_SELECTOR, "button.viewad-contact-submit")
        driver.execute_script("arguments[0].click();", send_button)
        time.sleep(2)

        print(f"✅ Message sent successfully to: {url}")
    except Exception as e:
        print(f"❌ Error while sending message: {e}")


def main(url):
    driver = setup_driver()
    time.sleep(2)

    # Prompt for login if not detected
    if not is_logged_in(driver):
        print("⚠️ Not logged in. Please log in manually.")
        input("⏸ After logging in, press [Enter] to continue...")
        if not is_logged_in(driver):
            print("❌ Login not detected. Exiting.")
            driver.quit()
            return

    send_message(driver, url)

    input("\n⏸ Process finished. Press [Enter] to close browser...")
    driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python messenger.py <listing-url>")
        sys.exit(1)
    main(sys.argv[1])
