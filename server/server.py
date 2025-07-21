# server.py
from flask import Flask, request, jsonify
import os
import subprocess
import time

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename or f"video_{int(time.time())}.mp4"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    print(f"✅ Video saved to {save_path}")

    # Trigger main.py dynamically with subprocess and pass filename
    try:
        print("🚀 Calling main.py...")
        subprocess.run(["python", "main.py", filename], check=True)
        return jsonify({"message": f"Video '{filename}' uploaded and processed"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
