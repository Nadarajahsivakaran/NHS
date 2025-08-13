from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from datetime import datetime, timedelta, time, date

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/", methods=["GET"])
def get_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointments  ORDER BY id DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        appointments = [
            {
                **row,
                "date": str(row["date"]),
                "time": str(row["time"]),
                "booked_at": row["booked_at"].isoformat() if row.get("booked_at") else None
            }
            for row in rows
        ]

        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


@appointments_bp.route("/", methods=["POST"])
def add_appointment():
    data = request.get_json()
    date = data.get("date")
    time = data.get("time")
    reason = data.get("reason")
    userid = data.get("id")

    if not all([date, time, reason, userid]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (userid, date, time, reason) VALUES (%s, %s, %s, %s)",
            (userid, date, time, reason),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment booked"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to insert", "details": str(e)}), 500


@appointments_bp.route("/<int:id>", methods=["PUT"])
def update_appointment(id):
    data = request.get_json()
    date = data.get("date")
    time = data.get("time")
    reason = data.get("reason")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE appointments SET date = %s, time = %s, reason = %s WHERE id = %s",
            (date, time, reason, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment updated"}), 200
    except Exception as e:
        return jsonify({"error": "Update failed", "details": str(e)}), 500


@appointments_bp.route("/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET isDelete = 1 WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment cancelled (soft deleted)"}), 200
    except Exception as e:
        return jsonify({"error": "Delete failed", "details": str(e)}), 500
