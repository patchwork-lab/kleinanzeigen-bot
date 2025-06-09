from flask import Flask, request
import subprocess
import os
import sys

# Initialize the Flask server
app = Flask(__name__)

# Define the POST endpoint '/send' which receives ad URLs


@app.route("/send", methods=["POST"])
def handle_send():
    data = request.json
    url = data.get("url")

    if not url:
        return "❌ Missing 'url' in request", 400

    print(f"📨 Incoming trigger → launching messenger.py for ad: {url}")

    try:
        # Use Python binary from current virtual environment
        venv_python = os.path.join(sys.prefix, "bin", "python")

        # Start messenger.py with the URL (non-blocking subprocess)
        subprocess.Popen([venv_python, "messenger.py", url])
        return "OK", 200
    except Exception as e:
        print(f"❌ Failed to start messenger.py: {e}")
        return "❌ Failed to launch subprocess", 500


# Run Flask API on http://localhost:5000
if __name__ == "__main__":
    print("🚀 API server running at http://localhost:5000 ...")
    app.run(port=5000)
