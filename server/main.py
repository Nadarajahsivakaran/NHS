import os
from app.video_processor import extract_audio_from_video
from app.speech_to_text import transcribe_audio
from app.translator import translate_to_english
from app.nlp_processor import analyze_text

VIDEO_PATH = "uploads/4.mp4"  # Replace with your video

def run_pipeline(video_path):
    print("[1] Extracting audio...")
    audio_path = extract_audio_from_video(video_path)

    print("[2] Transcribing audio...")
    text, lang_code, lang_name, verify_code = transcribe_audio(audio_path)
    print(f"✅ Detected Primary Language (Whisper): {lang_name} ({lang_code})")
    print(f"🧪 Verified Language from Text (langdetect): {verify_code}")
    print(f"📝 Transcription:\n{text}\n")

    print("[3] Translating to English...")
    english_text = translate_to_english(text, lang_code)
    print(f"🌍 Translated Text:\n{english_text}\n")

    print("[4] Running NLP analysis...")
    summary = analyze_text(english_text)
    print(f"🧠 NLP Summary:\n{summary}")

    # Save results
    with open("outputs/result.txt", "w", encoding="utf-8") as f:
        f.write(f"== Detected Language (Whisper) ==\n{lang_name} ({lang_code})\n")
        f.write(f"== Verified Language from Text (langdetect) ==\n{verify_code}\n\n")
        f.write("== Transcription ==\n")
        f.write(text + "\n\n")
        f.write("== Translated to English ==\n")
        f.write(english_text + "\n\n")
        f.write("== NLP Summary ==\n")
        f.write(summary)

    print("\n✅ All processing complete. Results saved to outputs/result.txt")

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    run_pipeline(VIDEO_PATH)
