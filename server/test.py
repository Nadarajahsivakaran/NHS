import os
from call_transcribe_api import transcribe_file

filename = '4.mp4'
file_path = os.path.join("uploads", filename)
print(f"📄 Filename: {filename}", flush=True)
print(f"📂 File path: {file_path}", flush=True)
transcribe_file(file_path)
