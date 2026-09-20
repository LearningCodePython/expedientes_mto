import os
import sqlite3
import json
from functools import wraps
from flask import Flask, render_template_string, request, jsonify, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "plantilla-mto-secret-key-2026-secure"
DB_PATH = "racks.db"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "No autorizado. Inicie sesión."}), 401
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        hashed_pw = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", hashed_pw))

    # Table for company configuration
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            tagline TEXT,
            logo_image TEXT,
            logo_text TEXT
        )
    """)
    
    # Table for racks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS racks (
            rack_id TEXT PRIMARY KEY,
            client TEXT,
            location TEXT,
            date TEXT,
            technician TEXT,
            front_photo TEXT,
            rear_photo TEXT,
            qr_code TEXT,
            notes TEXT,
            checklist TEXT,
            units TEXT,
            electronics TEXT,
            sort_order INTEGER
        )
    """)
    try:
        cursor.execute("ALTER TABLE racks ADD COLUMN electronics TEXT")
    except sqlite3.OperationalError:
        pass
    
    # Seed default company if empty
    cursor.execute("SELECT COUNT(*) FROM company")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO company (id, name, tagline, logo_image, logo_text)
            VALUES (1, 'Soportia IT - Infraestructura y Racks', 'Departamento de Mantenimiento y Certificación de Comunicaciones', NULL, 'SOP')
        """)
        
    # Seed default rack if empty
    cursor.execute("SELECT COUNT(*) FROM racks")
    if cursor.fetchone()[0] == 0:
        default_units = json.dumps({
            "42": "Patch Panel Fibra Óptica (Core)",
            "41": "Patch Panel Cat6A (Puestos 1-24)",
            "40": "Patch Panel Cat6A (Puestos 25-48)",
            "39": "Organizador de Cables 1U",
            "38": "Switch Core Cisco Catalyst 9300",
            "37": "Switch Distribución Planta 1",
            "36": "Router Perimetral BGP",
            "35": "Firewall UTM Fortinet 200F",
            "20": "Servidor Rack Dell PowerEdge R750",
            "19": "Servidor Rack Dell PowerEdge R740",
            "18": "Cabina de Almacenamiento NAS Synology",
            "5": "SAI / UPS APC Smart-RT 3000VA (Batería Principal)",
            "4": "SAI / UPS APC Smart-RT 3000VA (Módulo Extensión)",
            "1": "Bandeja de Accesorios y Puesta a Tierra General"
        })
        default_chk = json.dumps({
            "cabling": True,
            "power": True,
            "temperature": True,
            "labeling": True,
            "grounding": True
        })
        default_electronics = json.dumps([
            {"unit": "38", "id": "SW-CORE-01", "name": "Switch Core Cisco Catalyst 9300", "brand": "Cisco", "model": "Catalyst 9300", "serial": "FOC2548X92A", "mac": "00:1A:2B:3C:4D:5E"},
            {"unit": "37", "id": "SW-DIST-01", "name": "Switch Distribución Planta 1", "brand": "Cisco", "model": "Catalyst 3850", "serial": "FCW2310L014", "mac": "00:1A:2B:3C:4D:5F"},
            {"unit": "36", "id": "RT-PERI-01", "name": "Router Perimetral BGP", "brand": "Cisco", "model": "ISR 4331", "serial": "FTX2412058B", "mac": "00:1A:2B:3C:4D:60"},
            {"unit": "35", "id": "FW-UTM-01", "name": "Firewall UTM Fortinet 200F", "brand": "Fortinet", "model": "FortiGate 200F", "serial": "FG200F3Z21001234", "mac": "90:6C:AC:12:34:56"}
        ])
        cursor.execute("""
            INSERT INTO racks (rack_id, client, location, date, technician, front_photo, rear_photo, qr_code, notes, checklist, units, electronics, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "RACK-HQ-01",
            "Sede Central - Centro de Datos",
            "Sala Servidores Principal - Rack 01 (Fila A)",
            "2026-09-19",
            "Carlos Mendoza (Ing. Soporte)",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&auto=format&fit=crop&q=60",
            "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://app.soportia.com/rack/RACK-HQ-01",
            "Mantenimiento preventivo trimestral completado con éxito. Sustitución de ventiladores en switch core y revisión termográfica sin incidencias.",
            default_chk,
            default_units,
            default_electronics,
            0
        ))
        
    conn.commit()
    conn.close()

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/check-auth", methods=["GET"])
def check_auth():
    if "username" in session:
        return jsonify({"authenticated": True, "username": session["username"]})
    return jsonify({"authenticated": False})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or request.form
    if not data:
        return jsonify({"error": "No data provided"}), 400
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row[0], password):
        session["username"] = username
        return jsonify({"status": "success", "username": username})
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"status": "success"})

@app.route("/api/change-password", methods=["POST"])
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
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row or not check_password_hash(row[0], current_password):
        conn.close()
        return jsonify({"error": "La contraseña actual es incorrecta"}), 400
        
    new_hashed = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed, username))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

@app.route("/api/data", methods=["GET"])
@login_required
def get_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, tagline, logo_image, logo_text FROM company WHERE id = 1")
    comp_row = cursor.fetchone()
    company = {
        "name": comp_row["name"],
        "tagline": comp_row["tagline"],
        "logoImage": comp_row["logo_image"],
        "logoText": comp_row["logo_text"]
    }
    
    cursor.execute("SELECT * FROM racks ORDER BY sort_order ASC, rack_id ASC")
    rack_rows = cursor.fetchall()
    racks = []
    for row in rack_rows:
        racks.append({
            "id": row["rack_id"],
            "client": row["client"],
            "location": row["location"],
            "date": row["date"],
            "technician": row["technician"],
            "frontPhoto": row["front_photo"],
            "rearPhoto": row["rear_photo"],
            "qrCode": row["qr_code"],
            "notes": row["notes"],
            "checklist": json.loads(row["checklist"]) if row["checklist"] else {},
            "units": json.loads(row["units"]) if row["units"] else {},
            "electronics": json.loads(row["electronics"]) if "electronics" in row.keys() and row["electronics"] else []
        })
        
    conn.close()
    return jsonify({"company": company, "racks": racks})

@app.route("/api/data", methods=["POST"])
@login_required
def save_data():
    req = request.json
    if not req:
        return jsonify({"error": "No JSON data provided"}), 400
        
    company = req.get("company", {})
    racks = req.get("racks", [])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Update company
    cursor.execute("""
        UPDATE company 
        SET name = ?, tagline = ?, logo_image = ?, logo_text = ?
        WHERE id = 1
    """, (
        company.get("name"),
        company.get("tagline"),
        company.get("logoImage"),
        company.get("logoText", "SOP")
    ))
    
    # Replace all racks
    cursor.execute("DELETE FROM racks")
    for idx, rack in enumerate(racks):
        cursor.execute("""
            INSERT INTO racks (rack_id, client, location, date, technician, front_photo, rear_photo, qr_code, notes, checklist, units, electronics, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rack.get("id"),
            rack.get("client"),
            rack.get("location"),
            rack.get("date"),
            rack.get("technician"),
            rack.get("frontPhoto"),
            rack.get("rearPhoto"),
            rack.get("qrCode"),
            rack.get("notes"),
            json.dumps(rack.get("checklist", {})),
            json.dumps(rack.get("units", {})),
            json.dumps(rack.get("electronics", [])),
            idx
        ))
        
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    rack_id = request.form.get("rack_id") or (request.json and request.json.get("rack_id"))
    
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            os.makedirs("uploads", exist_ok=True)
            safe_rack_id = "".join(c if c.isalnum() else "_" for c in (rack_id or "rack"))
            filename = f"qr_{safe_rack_id}_{file.filename}"
            filepath = os.path.join("uploads", filename)
            file.save(filepath)
            return jsonify({"status": "success", "url": f"/{filepath}"})
            
    if request.is_json and request.json.get("image"):
        image_data = request.json.get("image")
        return jsonify({"status": "success", "url": image_data})
        
    return jsonify({"error": "No file or image provided"}), 400

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
