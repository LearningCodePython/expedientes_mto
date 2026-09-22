# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Tech Stack & Architecture
- **Backend**: Python Flask (`app.py`) running on port `5001`. Auto-initializes SQLite database at `data/racks.db` with default credentials (`admin` / `admin123`).
- **Frontend**: Single-file interface (`index.html`) using Tailwind CSS and FontAwesome, interacting via REST API (`/api/data`, `/api/login`, `/upload`).
- **Deployment**: Docker container (`Dockerfile`, `docker-compose.yml`) exposing port `5001`. Volumes required for persistence: `data/racks.db` and `uploads/`.

## Developer Commands
- **Start Server**: `pip3 install -r requirements.txt && python3 app.py` (`http://localhost:5001`)
- **Docker Dev**: `docker-compose up --build`

## Core Conventions & Rules
- **Persistence**: State and records persist via `/api/data` POST endpoints into SQLite (`data/racks.db`).
- **File Uploads**: Uploaded images (photos/QR) are saved in the `uploads/` directory.
- **Authentication**: Session-based auth via `/api/login`, `/api/logout`, `/api/check-auth`, `/api/change-password`.
- **Documentation Workflow**: When asked to **document** work, update `release.md` with recent milestones and commit changes.
