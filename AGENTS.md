# Project: Plantilla de Mantenimiento de Racks (`plantilla_mto`)

## Tech Stack & Architecture
- **Backend/Entrypoint**: Python Flask (`app.py`) on port `5001`.
- **Database**: SQLite at `data/racks.db` (auto-initializes with default credentials `admin` / `admin123`).
- **Frontend**: Single-file UI (`index.html`) using Tailwind CSS, communicating via REST API (`/api/data`, `/api/login`, `/upload`).
- **Uploads**: Saved in `uploads/` directory.

## Developer Commands
- **Start Server**: `pip3 install -r requirements.txt && python3 app.py`
- **Docker Dev**: `docker-compose up --build`
- **Run Tests**: `pytest`

## Core Rules & Workflows
- **Authentication**: Session-based auth via `/api/login`, `/api/logout`, `/api/check-auth`, `/api/change-password`.
- **Documentation**: When asked to **document** work, update `release.md` with recent milestones and commit changes.

## Architectural Improvement Roadmap (Step-by-Step)
1. **Paso 1: Implementación de Pruebas Automatizadas (`pytest`)** (Completado en v0.17.0)
2. **Paso 2: Modularización del Backend con Flask Blueprints** (Completado en v0.18.0)
3. **Paso 3: Abstracción de Base de Datos Configurable** (Completado en v0.19.0)
   - Soporte mediante variables de entorno (`DB_TYPE`, `DATABASE_URL`) para transicionar opcionalmente de SQLite a bases de datos relacionales escalables (PostgreSQL) en despliegues distribuidos.
4. **Paso 4: Validación y Versionado en `release.md`** (Completado en v0.19.0)
   - Registro de hitos superados y verificación de pruebas automatizadas en cada paso incremental.
