import speech_recognition as sr
from pydub import AudioSegment
import io

def transcribe_audio(audio_bytes: bytes) -> str:
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")  # Use "wav" or "ogg" if needed
        audio.export("temp.wav", format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return ""
