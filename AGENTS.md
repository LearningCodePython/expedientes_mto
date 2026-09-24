# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Tech Stack & Architecture
- **Backend/Entrypoint**: Python Flask (`app.py`) on port `5001`.
- **Database**: SQLite at `data/racks.db` (auto-initializes with default credentials `admin` / `admin123`).
- **Frontend**: Single-file UI (`index.html`) using Tailwind CSS, communicating via REST API (`/api/data`, `/api/login`, `/upload`).
- **Uploads**: Saved in `uploads/` directory.

## Developer Commands
- **Start Server**: `pip3 install -r requirements.txt && python3 app.py`
- **Docker Dev**: `docker-compose up --build`

## Core Rules & Workflows
- **Authentication**: Session-based auth via `/api/login`, `/api/logout`, `/api/check-auth`, `/api/change-password`.
- **Documentation**: When asked to **document** work, update `release.md` with recent milestones and commit changes.
