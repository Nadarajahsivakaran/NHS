# main.py

from call_transcribe_api import transcribe_file

if __name__ == '__main__':
    file_path = "uploads/4.mp4"
    transcribe_file(file_path)
