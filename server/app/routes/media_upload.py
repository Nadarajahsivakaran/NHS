# from flask import Blueprint, request, jsonify, current_app
# from werkzeug.utils import secure_filename
# from app.db import get_db_connection
# from datetime import datetime
# from call_transcribe_api import transcribe_file  # ✅ Direct import
# import os
# import time
#
# upload_bp = Blueprint("upload", __name__)
#
# @upload_bp.route("/", methods=["POST"])
# def upload_video():
#     file = request.files.get("file")
#     email = request.form.get("email")
#     timestamp = request.form.get("timestamp")
#
#     if not file or not email:
#         return jsonify({"error": "Missing file or email"}), 400
#
#     filename = secure_filename(file.filename or f"video_{int(time.time())}.mp4")
#     save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
#     file.save(save_path)
#     print(f"✅ Video saved to {save_path}")
#
#     # Get metadata
#     latitude = request.form.get("latitude")
#     longitude = request.form.get("longitude")
#
#     try:
#         dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")) if timestamp else datetime.now()
#     except ValueError as e:
#         return jsonify({"error": "Invalid timestamp format", "details": str(e)}), 400
#
#     # Get user ID (optional fallback = 0)
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
#     user = cursor.fetchone()
#     user_id = user[0] if user else 0
#
#     # Save initial video metadata (without transcript)
#     try:
#         cursor.execute("""
#             INSERT INTO videos (filename, uploaded_at, user_id, latitude, longitude, email)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (filename, dt, user_id, latitude, longitude, email))
#         video_id = cursor.lastrowid
#         conn.commit()
#         print("✅ Metadata saved to DB")
#     except Exception as e:
#         conn.rollback()
#         cursor.close()
#         conn.close()
#         return jsonify({"error": "DB insert failed", "details": str(e)}), 500
#
#     # Transcribe and update transcript + other details
#     try:
#         print("🚀 Running transcription process...")
#         result = transcribe_file(save_path)
#         if result is None:
#             raise Exception("Transcription API failed")
#
#         language = result.get("language", "")
#         transcription = result.get("transcription", "")
#         summary = result.get("translation", "")
#
#         # Update the video record with transcription results and status
#         cursor.execute("""
#             UPDATE videos
#             SET language = %s, transcription = %s, summary = %s, status = %s
#             WHERE id = %s
#         """, (language, transcription, summary, 1, video_id))
#         conn.commit()
#         print("📝 Transcription details saved to DB")
#
#         return jsonify({
#             "message": f"Video '{filename}' uploaded and processed",
#             "language": language,
#             "transcription": transcription,
#             "summary": summary
#         }), 200
#
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"error": "Processing failed", "details": str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()
#


from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.db import get_db_connection
from datetime import datetime
import os
import time

from tasks import transcribe_video_task  # import celery task

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["POST"])
def upload_video():
    file = request.files.get("file")
    email = request.form.get("email")
    timestamp = request.form.get("timestamp")

    if not file or not email:
        return jsonify({"error": "Missing file or email"}), 400

    filename = secure_filename(file.filename or f"video_{int(time.time())}.mp4")
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)
    print(f"✅ Video saved to {save_path}")

    # Get metadata
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")) if timestamp else datetime.now()
    except ValueError as e:
        return jsonify({"error": "Invalid timestamp format", "details": str(e)}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    user_id = user[0] if user else 0

    try:
        cursor.execute("""
            INSERT INTO videos (filename, uploaded_at, user_id, latitude, longitude, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (filename, dt, user_id, latitude, longitude, email))
        video_id = cursor.lastrowid
        conn.commit()
        print("✅ Metadata saved to DB")
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"error": "DB insert failed", "details": str(e)}), 500

    cursor.close()
    conn.close()

    # Enqueue transcription task asynchronously
    transcribe_video_task.delay(video_id, save_path)

    # Return response immediately (202 Accepted)
    return jsonify({
        "message": f"Video '{filename}' uploaded successfully. Transcription started in background."
    }), 202
