# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Context
- IT maintenance company performing on-site and corrective maintenance on client communication racks.
- Goal: Create a documentation template and application for a maintenance logbook.

## Architecture & Tech Stack
- **Backend**: Python Flask (`app.py`) running on port `5001`.
- **Database**: External SQLite database (`racks.db`) storing company configuration and rack records (photos, checklists, notes, 42U schema units).
- **Frontend**: Responsive web UI (`index.html`) using Tailwind CSS and REST API communication (`/api/data`).

## Developer Commands
- Start server: `python3 app.py` (accessible at `http://localhost:5001`).

## Rack Page Specifications
Each rack page must include:
- **Fixed Elements**: Company logo, header, and footer.
- **Uploadable / Dynamic Assets**:
  - Minimum 2 photos: Front view and rear view.
  - QR code image (linking to developed mobile app).
  - Rack diagram / schema (up to 42U).
- **Text & Notes**:
  - Brief location description.
  - Technician notes section at the bottom.
- **Export**: Full support for exporting the maintenance book / pages to PDF via CSS print styles (`@media print`).
