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
                "name": user["name"]
            }
        }), 200
    except Exception as e:
        return jsonify({"error": "Login error", "details": str(e)}), 500
