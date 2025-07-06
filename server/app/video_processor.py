import ffmpeg
from app.config import TEMP_AUDIO_PATH

def extract_audio_from_video(video_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(TEMP_AUDIO_PATH, ac=1, ar=16000)
            .run(overwrite_output=True)
        )
        return TEMP_AUDIO_PATH
    except Exception as e:
        print(f"Audio extraction failed: {e}")
        return None
