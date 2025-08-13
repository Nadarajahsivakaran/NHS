from celery_worker import celery
from call_transcribe_api import transcribe_file
from app.db import get_db_connection

@celery.task(bind=True)
def transcribe_video_task(self, video_id, file_path):
    try:
        result = transcribe_file(file_path)
        if not result:
            raise Exception("Transcription API failed")

        language = result.get("language", "")
        transcription = result.get("transcription", "")
        summary = result.get("translation", "")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE videos 
            SET language = %s, transcription = %s, summary = %s, status = %s
            WHERE id = %s
        """, (language, transcription, summary, 1, video_id))
        conn.commit()
    except Exception as e:
        # Optional: log failure or update DB status to failed
        print(f"Task failed: {e}")
    finally:
        cursor.close()
        conn.close()
