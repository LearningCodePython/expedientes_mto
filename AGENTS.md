# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Architecture & Tech Stack
- **Backend**: Python Flask (`app.py`) running on port `5001`. Auto-initializes SQLite (`racks.db`) with seed data on startup.
- **Database**: SQLite (`racks.db`) storing company configuration, rack metadata, 42U unit schemas (6 columns x 7 units), inventory/electronics, and verification checklists.
- **Frontend**: Single-file responsive UI (`index.html`) using Tailwind CSS, communicating via REST API (`/api/data` GET/POST and `/upload`).

## Developer & Operational Commands
- **Start Server**: `python3 app.py` (accessible at `http://localhost:5001`)

## Core Domain Rules & Specifications
- **Persistence**: State changes (branding, rack edits, 42U units, electronics, checklists) persist via `/api/data` POST. File uploads (QR codes/images) go to `/upload` and are saved in `uploads/`.
- **Views**: Supports Database Record view, Field Maintenance template view (for in-situ manual notes), and Network Electronics detail view.
- **PDF Export**: Multi-page maintenance report export optimized for A4 via CSS print styles (`@media print`).

## Workflow: Documentación
- Cuando pida **documentar** tu trabajo: actualizar `release.md` con los hitos recientes y ejecutar el commit correspondiente al repositorio.

## Objetivos Pendientes (Roadmap)
- Exposición en dominio público (`https://expedientes.cremheda.online`) con Coolify y SSL (puerto 443).
