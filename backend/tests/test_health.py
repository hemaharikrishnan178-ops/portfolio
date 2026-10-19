import pytest

from app import create_app
from app.extensions import db
from app.models.contact_message import ContactMessage
from app.models.project import Project
from app.routes.main import _rate_limit_store
from app.services.seed import seed_database


@pytest.fixture
def app():
    _rate_limit_store.clear()
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "CONTACT_RATE_LIMIT_SECONDS": 30,
        }
    )
    with application.app_context():
        db.create_all()
        seed_database()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()
    _rate_limit_store.clear()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check_reports_connected_database(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["database"] == "connected"


def test_projects_api_returns_only_the_two_portfolio_projects(client, app):
    with app.app_context():
        db.session.add(
            Project(
                title="Unlisted project",
                slug="unlisted-project",
                category="Test",
                description="Should not appear in the portfolio API.",
                technologies="Python",
                status="active",
            )
        )
        db.session.commit()

    response = client.get("/api/projects")

    assert response.status_code == 200
    projects = response.json["projects"]
    assert [project["slug"] for project in projects] == ["trustshare", "uzhavan-ai"]
    assert projects[0]["title"] == "TrustShare — Secure File-Sharing Platform"
    assert projects[1]["title"] == "Uzhavan AI — Intelligent Farming Companion"
    assert projects[0]["repository_url"] is None


def test_contact_submission_is_validated_and_persisted(client, app):
    payload = {
        "name": "Test Visitor",
        "email": "visitor@example.com",
        "subject": "Portfolio inquiry",
        "message": "This is a test message.",
    }

    response = client.post("/api/contact", json=payload)

    assert response.status_code == 201
    assert response.json["message"] == "Message sent successfully."
    with app.app_context():
        stored_message = db.session.query(ContactMessage).one()
        assert stored_message.name == payload["name"]
        assert stored_message.email == payload["email"]
        assert stored_message.message == payload["message"]


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "email": "person@example.com", "subject": "Hello", "message": "Message"},
        {"name": "Visitor", "email": "invalid", "subject": "Hello", "message": "Message"},
        {"name": 42, "email": "person@example.com", "subject": "Hello", "message": "Message"},
        {"name": "Visitor", "email": "person@example.com", "subject": "Hello", "message": "x" * 1201},
    ],
)
def test_invalid_contact_payload_is_rejected_without_storing(client, app, payload):
    response = client.post("/api/contact", json=payload)

    assert response.status_code == 400
    with app.app_context():
        assert db.session.query(ContactMessage).count() == 0


def test_contact_endpoint_rate_limits_repeated_submissions(client):
    payload = {
        "name": "Test Visitor",
        "email": "visitor@example.com",
        "subject": "Portfolio inquiry",
        "message": "This is a test message.",
    }

    assert client.post("/api/contact", json=payload).status_code == 201
    response = client.post("/api/contact", json=payload)

    assert response.status_code == 429


def test_production_database_urls_use_psycopg(monkeypatch):
    from app.config.settings import get_settings

    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("SECRET_KEY", "test-only-secret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@example.test:5432/portfolio")
    monkeypatch.setenv("FRONTEND_ORIGINS", "https://portfolio.example.test")

    settings = get_settings()

    assert settings["SQLALCHEMY_DATABASE_URI"] == (
        "postgresql+psycopg://user:password@example.test:5432/portfolio"
    )
    assert settings["CORS_ORIGINS"] == ["https://portfolio.example.test"]
