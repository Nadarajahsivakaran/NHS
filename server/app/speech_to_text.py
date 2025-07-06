import whisper
import pycountry
from langdetect import detect

model = whisper.load_model("small")  # use "medium" or "large"

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    text = result["text"]
    language_code = result["language"]

    # Confirm with langdetect if needed
    try:
        verify_code = detect(text)
    except:
        verify_code = "unknown"

    # Convert language code to full name
    try:
        language_name = pycountry.languages.get(alpha_2=language_code).name
    except:
        language_name = "Unknown"

    return text, language_code, language_name, verify_code
