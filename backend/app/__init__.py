from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.config.settings import get_settings
from app.extensions import db
from app.routes.main import main_bp
from app.services.seed import seed_database


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    settings = get_settings()
    app.config.update(settings)
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    app.register_blueprint(main_bp)

    @app.route("/")
    def index():
        return {"message": "Portfolio API is running."}, 200

    @app.cli.command("seed")
    def seed_command():
        seed_database()

    return app


__all__ = ["create_app"]
