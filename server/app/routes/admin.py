from flask import Blueprint, jsonify,request
from app.db import get_db_connection
from datetime import datetime, date, time, timedelta

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/appointments", methods=["GET"])
def get_all_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                a.id, a.date, a.time, a.reason, DATE(a.booked_at) AS booked_at_date, 
                a.isDelete, a.isApproved,
                u.id AS user_id, u.name
            FROM appointments a
            JOIN users u ON a.userid = u.id
            ORDER BY a.date DESC, a.time DESC
        """)

        appointments = cursor.fetchall()

        for appt in appointments:
            if isinstance(appt.get("date"), (date, datetime)):
                appt["date"] = appt["date"].isoformat()

            if isinstance(appt.get("time"), (time, datetime, timedelta)):
                t = appt["time"]
                if isinstance(t, timedelta):
                    total_seconds = int(t.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    appt["time"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    appt["time"] = t.isoformat()

            if isinstance(appt.get("booked_at_date"), (date, datetime)):
                appt["booked_at_date"] = appt["booked_at_date"].isoformat()

        cursor.close()
        conn.close()

        return jsonify(appointments), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch appointments", "details": str(e)}), 500


@admin_bp.route("/emergency-reports", methods=["GET"])
def get_all_emergency_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                er.id, er.email, er.filename, er.uploaded_at, er.status, 
                er.latitude, er.longitude,er.language,er.transcription,er.summary,
                u.id AS user_id, u.name
            FROM videos er
            LEFT JOIN users u ON er.user_id = u.id
            ORDER BY er.uploaded_at DESC
        """)

        reports = cursor.fetchall()

        for report in reports:
            if isinstance(report.get("uploaded_at"), datetime):
                report["uploaded_at"] = report["uploaded_at"].isoformat()

        cursor.close()
        conn.close()

        return jsonify(reports), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch emergency reports", "details": str(e)}), 500


@admin_bp.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    try:
        data = request.get_json()
        if not data or "isApproved" not in data:
            return jsonify({"error": "'isApproved' field is required"}), 400

        is_approved = data["isApproved"]

        if is_approved not in [0, 1, 2]:
            return jsonify({"error": "Invalid 'isApproved' value. Allowed: 0, 1, 2"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            cursor.close()
            conn.close()
            return jsonify({"error": "Appointment not found"}), 404

        cursor.execute("""
            UPDATE appointments
            SET isApproved = %s
            WHERE id = %s
        """, (is_approved, appointment_id))
        conn.commit()

        cursor.execute("""
            SELECT 
                a.id, a.date, a.time, a.reason, DATE(a.booked_at) AS booked_at_date,
                a.isDelete, a.isApproved,
                u.id AS user_id, u.name
            FROM appointments a
            JOIN users u ON a.userid = u.id
            WHERE a.id = %s
        """, (appointment_id,))

        updated = cursor.fetchone()

        if isinstance(updated.get("date"), (date, datetime)):
            updated["date"] = updated["date"].isoformat()
        if isinstance(updated.get("time"), (time, datetime, timedelta)):
            t = updated["time"]
            if isinstance(t, timedelta):
                total_seconds = int(t.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                updated["time"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                updated["time"] = t.isoformat()
        if isinstance(updated.get("booked_at_date"), (date, datetime)):
            updated["booked_at_date"] = updated["booked_at_date"].isoformat()

        cursor.close()
        conn.close()

        return jsonify(updated), 200

    except Exception as e:
        return jsonify({"error": "Failed to update appointment", "details": str(e)}), 500