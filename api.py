# api.py
# Einfacher Flask-Server, der POST-Anfragen von scraper.py entgegennimmt
# und bei einer neuen Anzeige messenger.py mit der URL startet

from flask import Flask, request
import subprocess

# Flask-App initialisieren
app = Flask(__name__)

# Definiere einen Endpunkt '/send', der POST-Anfragen akzeptiert
@app.route("/send", methods=["POST"])
def handle_send():
    # Erwartet JSON-Daten mit dem Schlüssel "url"
    data = request.json
    url = data.get("url")

    # Falls keine URL übergeben wurde, antworte mit einem Fehler
    if not url:
        return "Fehlende URL in Anfrage", 400

    # Logge im Terminal, welche URL verarbeitet werden soll
    print(f"Ausgehender Trigger: Starte Messenger für Anzeige → {url}")

    try:
        # Starte messenger.py mit der URL als Argument in einem neuen Subprozess
        # Popen = asynchroner Aufruf (nicht blockierend für den Server)
        subprocess.Popen(["python3", "messenger.py", url])
        return "OK", 200  # Erfolgsmeldung an den Aufrufer (z. B. scraper.py)
    except Exception as e:
        # Fehler beim Starten des Subprozesses
        print(f"Fehler beim Starten von messenger.py: {e}")
        return "Fehler beim Starten des Prozesses", 500

# Startet den Server auf Port 5000, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    print("API-Server läuft auf http://localhost:5000 ...")
    app.run(port=5000)