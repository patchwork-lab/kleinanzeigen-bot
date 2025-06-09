from flask import Flask, request
import subprocess
import os
import sys

app = Flask(__name__)


@app.route("/send", methods=["POST"])
def handle_send():
    data = request.json
    url = data.get("url")

    if not url:
        return "Fehlende URL in Anfrage", 400

    print(f"Ausgehender Trigger: Starte Messenger für Anzeige → {url}")

    try:
        venv_python = os.path.join(sys.prefix, "bin", "python")
        subprocess.Popen([venv_python, "messenger.py", url])
        return "OK", 200
    except Exception as e:
        print(f"Fehler beim Starten von messenger.py: {e}")
        return "Fehler beim Starten des Prozesses", 500


if __name__ == "__main__":
    print("API-Server läuft auf http://localhost:5000 ...")
    app.run(port=5000)
