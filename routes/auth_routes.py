import sqlite3
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import services.db_service as db
from services.db_service import login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/check-auth", methods=["GET"])
def check_auth():
    if "username" in session:
        return jsonify({"authenticated": True, "username": session["username"]})
    return jsonify({"authenticated": False})

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json or request.form
    if not data:
        return jsonify({"error": "No data provided"}), 400
    username = data.get("username")
    password = data.get("password")
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row["password" if isinstance(row, dict) or hasattr(row, 'keys') else 0], password):
        session["username"] = username
        return jsonify({"status": "success", "username": username})
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"status": "success"})

@auth_bp.route("/api/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    if not current_password or not new_password:
        return jsonify({"error": "Faltan datos requeridos"}), 400
        
    username = session["username"]
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    stored_pw = row["password"] if isinstance(row, dict) or hasattr(row, 'keys') else row[0]
    if not row or not check_password_hash(stored_pw, current_password):
        conn.close()
        return jsonify({"error": "La contraseña actual es incorrecta"}), 400
        
    new_hashed = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed, username))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})
