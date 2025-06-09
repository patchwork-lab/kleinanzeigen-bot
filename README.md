# Kleinanzeigen-Bot

Ein Python-basierter Bot, der **automatisch auf neue Anzeigen auf kleinanzeigen.de reagiert** ideal z.B. für heiß begehrte Artikel. Sobald eine passende Anzeige erscheint, wird automatisch eine Nachricht an den Anbieter gesendet.

---

## Voraussetzungen

- Python 3.11 (empfohlen)
- `chromedriver` (installiert in deinem virtuellen Environment)
- Ein **Chrome-Profil mit aktivem Login bei Kleinanzeigen**

---

## Installation

1. Repository klonen:

   ```bash
   git clone https://github.com/dein-user/kleinanzeigen-bot.git
   cd kleinanzeigen-bot
   ```

2. Virtuelle Umgebung erstellen:

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Abhngigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

---

## Konfiguration

Erstelle eine Datei `.env` im Projektverzeichnis (Beispiel: siehe `.env.example`):

```env
EMAIL=dein@mail.de
PASSWORD=deinpasswort
MESSAGE_TEXT=Hi, ich habe Interesse! :)
CHROME_PROFILE_PATH=/Users/deinname/path/zum/chrome-profile
SEARCH_URL=https://www.kleinanzeigen.de/s-bender-statue/k0
BLACKLIST=fake,broken
```

---

## Chrome-Profil vorbereiten

Falls du dein aktives Chrome-Profil **nur fr den Bot verwenden mchtest**, gehe so vor:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --user-data-dir="/tmp/kleinanzeigen-profile" \
  --profile-directory=Default
```

1. Melde dich im geffneten Chrome bei Kleinanzeigen an.
2. Schliee Chrome.
3. Kopiere das Profil in dein Projektverzeichnis:

   ```bash
   cp -R /tmp/kleinanzeigen-profile ./chrome-profile
   ```

4. Trage den Pfad in deiner `.env` ein:
   ```env
   CHROME_PROFILE_PATH=/Users/deinname/deinprojektverzeichnis/chrome-profile
   ```

---

## Nutzung

### 1. API starten

```bash
python api.py
```

### 2. Scraper starten (durchsucht regelmig die Anzeigen):

```bash
python scraper.py
```

Wenn eine passende Anzeige erscheint, wird:

- berprft, ob sie bereits bekannt ist
- auf Blacklist gefiltert
- und **automatisch `messenger.py` mit der Anzeigen-URL aufgerufen**

## Optional Headless-Modus

- Wenn du den Bot im **unsichtbaren Headless-Modus** nutzen möchtest, kannst du in `messenger.py` in der Funktion `setup_driver()` die Zeile

  ```python
  options.headless = False
  ```

  durch

  ```python
  options.add_argument("--headless=new")
  ```

  ersetzen.

---

## Projektstruktur

```plaintext
kleinanzeigen-bot/

 api.py               # Flask-Server fr Kommunikation
 scraper.py           # Sucht regelmig nach neuen Anzeigen
 messenger.py         # Sendet Nachricht ber Chrome
 .env                 # Konfiguration (nicht in Git!)
 .env.example         # Beispielkonfiguration
 requirements.txt     # Python-Abhngigkeiten
 seen_ads.txt         # Bereits gesichtete Anzeigen
 ignored_ads.txt      # Anzeigen, die durch Blacklist gefiltert wurden
 chrome-profile/      # Gespeichertes Chrome-Profil mit Login
 README.md
```

---

## Hinweise

- Verwende den Bot verantwortungsvoll.
- Kleinanzeigen.de kann automatisierten Zugriff ggf. blockieren nutze Pausenintervalle und keine zu aggressive Frequenz.
- Projekt dient als Lern- und Automatisierungshilfe, keine Garantie auf Erfolg oder dauerhafte Funktionalitt.

---

## To Do (optional)

- Benutzer-Login über Eingabe statt `.env`
- Mehrfach-Absendeschutz
- Frontend-UI zur Verwaltung
- Erweiterte blacklist/ignore Logik

---

## Kontakt

Georg | [github.com/patchwork-lab](https://github.com/patchwork-lab)

---

---

---

# ENGLISH README VERSION

# Classified Ads Bot

A Python-based bot that **automatically responds to new listings on kleinanzeigen.de** – ideal for highly sought-after tickets. As soon as a suitable listing appears, a message is automatically sent to the seller.

---

## Requirements

- Python 3.11 (recommended)
- `chromedriver` (installed in your virtual environment)
- A **Chrome profile with an active login on Kleinanzeigen**

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dein-user/kleinanzeigen-bot.git
   cd kleinanzeigen-bot
   ```

2. Create a virtual environment:

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the project directory (example: see `.env.example`):

```env
EMAIL=your@mail.com
PASSWORD=yourpassword
MESSAGE_TEXT=Hi, I'm interested! :)
CHROME_PROFILE_PATH=/Users/yourname/path/to/chrome-profile
SEARCH_URL=https://www.kleinanzeigen.de/s-bender-statue/k0
BLACKLIST=fake,broken
```

---

## Preparing the Chrome Profile

If you want to use your active Chrome profile **only for the bot**, proceed as follows:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --user-data-dir="/tmp/kleinanzeigen-profile" \
  --profile-directory=Default
```

1. Log in to Kleinanzeigen in the opened Chrome window.
2. Close Chrome.
3. Copy the profile to your project directory:

   ```bash
   cp -R /tmp/kleinanzeigen-profile ./chrome-profile
   ```

4. Enter the path in your `.env` file:
   ```env
   CHROME_PROFILE_PATH=/Users/yourname/yourprojectdirectory/chrome-profile
   ```

---

## Usage

### 1. Start API

```bash
python api.py
```

### 2. Start Scraper (regularly searches listings):

```bash
python scraper.py
```

When a suitable listing appears, the bot:

- Checks whether it's already known
- Filters based on blacklist
- and **automatically calls `messenger.py` with the listing URL**

## Optional Headless-Mode

- If you want to use the bot in **invisible headless mode**, open `messenger.py` and change this line in the `setup_driver()` function:

  ```python
  options.headless = False
  ```

  to

  ```python
  options.add_argument("--headless=new")
  ```

---

## Project Structure

```plaintext
kleinanzeigen-bot/

 api.py               # Flask server for communication
 scraper.py           # Regularly searches for new listings
 messenger.py         # Sends message via Chrome
 .env                 # Configuration (not in Git!)
 .env.example         # Example configuration
 requirements.txt     # Python dependencies
 seen_ads.txt         # Already seen listings
 ignored_ads.txt      # Listings filtered by blacklist
 chrome-profile/      # Saved Chrome profile with login
 README.md
```

---

## Notes

- Use the bot responsibly.
- Kleinanzeigen.de may block automated access – use pause intervals and avoid aggressive frequency.
- This project is intended as a learning and automation aid, no guarantee of success or permanent functionality.

---

## To Do (optional)

- User login via input instead of `.env`
- Multiple send protection
- Frontend UI for management
- Extended blacklist/ignore logic

---

## Contact

Georg | [github.com/patchwork-lab](https://github.com/patchwork-lab)
