# call_transcribe_api.py
import requests
import os
import urllib3

# Disable SSL warning in dev
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NGROK_URL = "https://9108-34-142-246-12.ngrok-free.app/transcribe"  # Update as needed

def transcribe_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "video/mp4")}
            print(f"📤 Uploading {file_path} to {NGROK_URL}")

            response = requests.post(NGROK_URL, files=files, timeout=300, verify=False)

        response.raise_for_status()
        data = response.json()

        print("\n✅ Transcription Result:")
        print("Detected Language: ", data.get("language", "N/A"))
        print("Original Transcription:", data.get("transcription", "N/A"))
        print("Translation:", data.get("translation", "N/A"))
        print("Summary:", data.get("summary", "N/A"))
        print("Execution Time (s):", data.get("execution_time", "N/A"))

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
    except Exception as ex:
        print("❌ Other error:", ex)
