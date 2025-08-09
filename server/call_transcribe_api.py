# call_transcribe_api.py
import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
NGROK_URL = "https://427ed676e908.ngrok-free.app/transcribe"

def transcribe_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "video/mp4")}
        print(f"📤 Sending {file_path} to {NGROK_URL}")
        response = requests.post(NGROK_URL, files=files, timeout=300, verify=False)

    if response.ok:
        data = response.json()
        print("\n✅ Result:")
        print("Language:", data.get("language"))
        print("Transcription:", data.get("transcription"))
        print("Translation:", data.get("translation"))
        print("Summary:", data.get("summary"))
        print("Execution Time:", data.get("execution_time"))
        return data
    else:
        print("❌ Failed:", response.text)
        return None