import os
import sqlite3
import json
from functools import wraps
from flask import jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

os.makedirs("data", exist_ok=True)
DB_PATH = os.environ.get("DB_PATH", "data/racks.db")
DB_TYPE = os.environ.get("DB_TYPE", "sqlite").lower()
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """
    Abstracción de conexión de base de datos configurable.
    Soporta SQLite (por defecto) y PostgreSQL (mediante DATABASE_URL o DB_TYPE=postgres).
    """
    if DB_TYPE in ("postgres", "postgresql") or (DATABASE_URL and DATABASE_URL.startswith("postgres")):
        try:
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(DATABASE_URL or os.environ.get("DATABASE_URL"))
            return conn
        except ImportError:
            raise RuntimeError("psycopg2 no está instalado. Instálalo para usar PostgreSQL.")
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "No autorizado. Inicie sesión."}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "No autorizado. Inicie sesión."}), 401
        if session.get("role") != "admin":
            return jsonify({"error": "Acceso denegado. Se requieren privilegios de Administrador."}), 403
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    is_postgres = DB_TYPE in ("postgres", "postgresql") or (DATABASE_URL and DATABASE_URL.startswith("postgres"))
    conn = get_db_connection()
    
    if is_postgres:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(255) PRIMARY KEY,
                        password TEXT,
                        role VARCHAR(50) DEFAULT 'admin'
                    )
                """)
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'admin'")
                except Exception:
                    pass

                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    hashed_pw = generate_password_hash("admin123")
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("admin", hashed_pw, "admin"))

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS company (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        name TEXT,
                        tagline TEXT,
                        logo_image TEXT,
                        logo_text TEXT
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS racks (
                        rack_id VARCHAR(255) PRIMARY KEY,
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
                        sort_order INTEGER,
                        total_units INTEGER
                    )
                """)
                
                cursor.execute("SELECT COUNT(*) FROM company")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO company (id, name, tagline, logo_image, logo_text)
                        VALUES (1, 'Soportia IT - Infraestructura y Racks', 'Departamento de Mantenimiento y Certificación de Comunicaciones', NULL, 'SOP')
                    """)
                    
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
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    else:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT DEFAULT 'admin'
            )
        """)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'admin'")
        except sqlite3.OperationalError:
            pass

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            hashed_pw = generate_password_hash("admin123")
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", hashed_pw, "admin"))

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT,
                tagline TEXT,
                logo_image TEXT,
                logo_text TEXT
            )
        """)
        
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
                sort_order INTEGER,
                total_units INTEGER
            )
        """)
        try:
            cursor.execute("ALTER TABLE racks ADD COLUMN electronics TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute("ALTER TABLE racks ADD COLUMN total_units INTEGER")
        except sqlite3.OperationalError:
            pass
        
        cursor.execute("SELECT COUNT(*) FROM company")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO company (id, name, tagline, logo_image, logo_text)
                VALUES (1, 'Soportia IT - Infraestructura y Racks', 'Departamento de Mantenimiento y Certificación de Comunicaciones', NULL, 'SOP')
            """)
            
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
