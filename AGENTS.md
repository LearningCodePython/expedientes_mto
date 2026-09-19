# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Architecture & Tech Stack
- **Backend**: Python Flask (`app.py`) running on port `5001`. Auto-initializes SQLite database (`racks.db`) on startup with default company config and seed racks.
- **Database**: SQLite (`racks.db`) storing company branding, rack metadata, 42U unit schema, checklists, and base64/URL assets.
- **Frontend**: Single-file responsive web UI (`index.html`) using Tailwind CSS, communicating with REST API (`/api/data` GET/POST).

## Developer Commands
- **Start Server**: `python3 app.py` (`http://localhost:5001`)

## Core Domain Rules & Specifications
- **Data Persistence**: All state changes (company config, rack edits, 42U slots, checklists) persist via `/api/data` POST to SQLite (`racks.db`).
- **Rack Structure**: Each rack record manages 42U units, front/rear photos, QR codes, technician notes, and verification checklists (cabling, power, temperature, labeling, grounding).
- **PDF Export**: Full support for multi-page maintenance report export via CSS print styles (`@media print` for A4 layout).
