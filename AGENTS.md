# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Architecture & Tech Stack
- **Backend**: Python Flask (`app.py`) on port `5001`. Auto-initializes SQLite (`racks.db`) on startup.
- **Database**: SQLite (`racks.db`) storing company configuration, rack metadata, 42U unit schemas, inventory/electronics, checklists, and asset URLs/Base64 data.
- **Frontend**: Single-file responsive UI (`index.html`) with Tailwind CSS, communicating via REST API (`/api/data` GET/POST).

## Developer Commands
- **Start Server**: `python3 app.py` (`http://localhost:5001`)

## Core Domain Rules & Specifications
- **Persistence**: All state modifications (company branding, rack edits, 42U units, electronics, checklists) persist via `/api/data` POST.
- **Rack Structure**: 42U units, front/rear photos (9:16 container aspect ratio), QR codes, technician notes, inventory/electronics tracking, and verification checklists (cabling, power, temperature, labeling, grounding).
- **Views**: Supports both Database Record view and Field Maintenance template view.
- **PDF Export**: Multi-page maintenance report export via CSS print styles (`@media print` for A4 layout).

## Workflow: Documentación
- Cuando pida **documentar** tu trabajo: actualizar `release.md` con los hitos recientes y ejecutar el commit al repositorio.
