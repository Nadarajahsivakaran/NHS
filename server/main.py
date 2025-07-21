# main.py
import sys
import os
from call_transcribe_api import transcribe_file
import webbrowser  # Optional fallback
import subprocess
import platform


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No filename provided.")
        sys.exit(1)

    # filename = sys.argv[1]
    # file_path = f"uploads/5.mp4"
    filename = sys.argv[1]
    file_path = os.path.join("uploads", filename)
    print(f"📄 Filename: {filename}", flush=True)
    print(f"📂 File path: {file_path}", flush=True)
    transcribe_file(file_path)

# Try to open video with default player
try:
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", file_path])
    else:  # Linux
        subprocess.run(["xdg-open", file_path])
except Exception as e:
    print(f"❌ Could not open video file: {e}")
