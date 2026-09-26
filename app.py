import os
from flask import Flask
from services.db_service import init_db, DB_PATH
from routes.auth_routes import auth_bp
from routes.api_routes import api_bp

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "plantilla-mto-secret-key-2026-secure"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
