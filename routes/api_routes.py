import os
import sqlite3
import json
from flask import Blueprint, request, jsonify, send_from_directory
import services.db_service as db
from services.db_service import login_required

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@api_bp.route("/api/data", methods=["GET"])
@login_required
def get_data():
    conn = db.get_db_connection()
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
            "electronics": json.loads(row["electronics"]) if "electronics" in row.keys() and row["electronics"] else [],
            "totalUnits": row["total_units"] if "total_units" in row.keys() and row["total_units"] is not None else 42
        })
        
    conn.close()
    return jsonify({"company": company, "racks": racks})

@api_bp.route("/api/data", methods=["POST"])
@login_required
def save_data():
    req = request.json
    if not req:
        return jsonify({"error": "No JSON data provided"}), 400
        
    company = req.get("company", {})
    racks = req.get("racks", [])
    
    conn = db.get_db_connection()
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
            INSERT INTO racks (rack_id, client, location, date, technician, front_photo, rear_photo, qr_code, notes, checklist, units, electronics, sort_order, total_units)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            idx,
            rack.get("totalUnits", 42)
        ))
        
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@api_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    rack_id = request.form.get("rack_id") or (request.json and request.json.get("rack_id"))
    file_type = request.form.get("type") or "qr"
    
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            os.makedirs("uploads", exist_ok=True)
            safe_rack_id = "".join(c if c.isalnum() else "_" for c in (rack_id or "rack"))
            prefix = file_type if file_type in ["front", "rear", "qr"] else "img"
            filename = f"{prefix}_{safe_rack_id}_{file.filename}"
            filepath = os.path.join("uploads", filename)
            file.save(filepath)
            return jsonify({"status": "success", "url": f"/{filepath}"})
            
    if request.is_json and request.json.get("image"):
        image_data = request.json.get("image")
        return jsonify({"status": "success", "url": image_data})
        
    return jsonify({"error": "No file or image provided"}), 400

@api_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
