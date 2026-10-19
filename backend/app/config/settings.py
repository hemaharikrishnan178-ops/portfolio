import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_settings():
    environment = os.getenv("APP_ENV", "development").lower()
    database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_DATABASE_URL")
    if not database_url:
        database_url = f"sqlite:///{BASE_DIR / 'instance' / 'hema_portfolio.db'}"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    secret_key = os.getenv("SECRET_KEY")
    if environment == "production":
        if not secret_key:
            raise ValueError("SECRET_KEY must be configured in production.")
        if not database_url.startswith("postgresql+psycopg://"):
            raise ValueError("DATABASE_URL must point to PostgreSQL in production.")
    else:
        secret_key = secret_key or "dev-secret-key"

    origins_setting = os.getenv("FRONTEND_ORIGINS")
    if origins_setting is None:
        origins_setting = "" if environment == "production" else "http://localhost:5173,http://127.0.0.1:5173"
    frontend_origins = [
        origin.strip()
        for origin in origins_setting.split(",")
        if origin.strip()
    ]
    if environment == "production" and not frontend_origins:
        raise ValueError("FRONTEND_ORIGINS must include the deployed frontend origin in production.")

    return {
        "SECRET_KEY": secret_key,
        "APP_ENV": environment,
        "SQLALCHEMY_DATABASE_URI": database_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "CORS_ORIGINS": frontend_origins,
        "CONTACT_RATE_LIMIT_SECONDS": int(os.getenv("CONTACT_RATE_LIMIT_SECONDS", "30")),
        "JSON_SORT_KEYS": False,
    }
