from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection
import mysql.connector

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    passport = data.get("passport")
    email = data.get("email")
    password = data.get("password")
    mobile = data.get("mobile")
    postcode = data.get("postcode")

    if not name or not passport or not email or not password:
        return jsonify({"error": "Name, passport, email, and password are required."}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, passport, email, password, mobile, postcode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, passport, email, hashed_password, mobile, postcode))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully."}), 200
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email or passport number already exists."}), 409
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials."}), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "email": user["email"],
                "name": user["name"],
                "type": user["type"],
                "id": user["id"]
            }
        }), 200
    except Exception as e:
        return jsonify({"error": "Login error", "details": str(e)}), 500


@auth_bp.route("/user", methods=["PUT"])
def update_user():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404

        # Frontend keys to DB column mapping
        field_map = {
            "fullName": "name",
            "passportNumber": "passport",
            "mobile": "mobile",
            "postcode": "postcode"
        }

        fields_to_update = {
            db_field: data[front_key]
            for front_key, db_field in field_map.items()
            if front_key in data
        }

        if not fields_to_update:
            cursor.close()
            conn.close()
            return jsonify({"error": "No valid fields to update"}), 400

        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update])
        values = list(fields_to_update.values())
        values.append(email)  # for WHERE clause

        sql = f"UPDATE users SET {set_clause} WHERE email = %s"
        cursor.execute(sql, values)
        conn.commit()

        # Fetch updated user
        cursor.execute("SELECT name, passport, email, mobile, postcode FROM users WHERE email = %s", (email,))
        updated_user = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({"message": "User profile updated successfully", "user": updated_user}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@auth_bp.route("/user", methods=["post"])
def get_user():
    data = request.get_json()
    email = data.get("email") if data else None
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, passport, email, mobile, postcode FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@auth_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, passport, mobile, postcode, type FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"users": users}), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500



