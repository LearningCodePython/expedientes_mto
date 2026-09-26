import sqlite3
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import services.db_service as db
from services.db_service import login_required, admin_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/check-auth", methods=["GET"])
def check_auth():
    if "username" in session:
        return jsonify({
            "authenticated": True,
            "username": session["username"],
            "role": session.get("role", "admin")
        })
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
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
        
    stored_pw = row["password"] if isinstance(row, dict) or hasattr(row, 'keys') else row[0]
    stored_role = row["role"] if isinstance(row, dict) or hasattr(row, 'keys') else (row[1] if len(row) > 1 else "admin")
    
    if check_password_hash(stored_pw, password):
        session["username"] = username
        session["role"] = stored_role or "admin"
        return jsonify({"status": "success", "username": username, "role": session["role"]})
        
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("role", None)
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

@auth_bp.route("/api/users", methods=["GET"])
@admin_required
def list_users():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users ORDER BY username ASC")
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for r in rows:
        users.append({
            "username": r["username"] if isinstance(r, dict) or hasattr(r, 'keys') else r[0],
            "role": r["role"] if isinstance(r, dict) or hasattr(r, 'keys') else (r[1] if len(r) > 1 else "admin")
        })
    return jsonify({"users": users})

@auth_bp.route("/api/users", methods=["POST"])
@admin_required
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "readonly")
    
    if not username or not password:
        return jsonify({"error": "Faltan datos requeridos (usuario y contraseña)"}), 400
        
    if role not in ["admin", "readonly"]:
        role = "readonly"
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "El nombre de usuario ya existe"}), 400
        
    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "username": username, "role": role})

@auth_bp.route("/api/users/<username>", methods=["DELETE"])
@admin_required
def delete_user(username):
    if username == "admin":
        return jsonify({"error": "No se puede eliminar el usuario administrador principal"}), 400
        
    if username == session.get("username"):
        return jsonify({"error": "No puedes eliminar tu propio usuario activo"}), 400
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})
