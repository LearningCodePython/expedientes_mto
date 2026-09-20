# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Tech Stack & Architecture
- **Backend**: Python Flask (`app.py`) on port `5001`. Auto-initializes SQLite (`racks.db`) and session auth (default credentials: `admin` / `admin123`).
- **Frontend**: Single-file UI (`index.html`) using Tailwind CSS, communicating via REST API (`/api/data`, `/api/login`, `/upload`).
- **Deployment**: Docker container (`Dockerfile`, `docker-compose.yml`) exposing port `5001`. Ready for Coolify with persistent volumes for `racks.db` and `uploads/`.

## Developer Commands
- **Start Server**: `pip install -r requirements.txt && python3 app.py` (`http://localhost:5001`)
- **Docker Dev**: `docker-compose up --build`

## Core Conventions & Rules
- **Persistence & Uploads**: State persists via `/api/data` POST; file uploads go to `/upload` (saved in `uploads/`).
- **Auth**: Session-based auth via `/api/login`, `/api/logout`, `/api/check-auth`, `/api/change-password`.
- **Documentation Workflow**: When asked to **document** work, update `release.md` with recent milestones and commit changes.
