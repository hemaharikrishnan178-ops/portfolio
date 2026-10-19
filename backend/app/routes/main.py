from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.services.contact_service import save_contact_message, validate_contact_payload
from app.services.project_service import get_projects_data
from app.services.seed import get_skills_data

main_bp = Blueprint("main", __name__)
_rate_limit_store = {}


def _is_rate_limited(client_ip):
    import time

    limit_seconds = current_app.config.get("CONTACT_RATE_LIMIT_SECONDS", 30)
    now = time.time()
    last_time = _rate_limit_store.get(client_ip, 0)
    if now - last_time < limit_seconds:
        return True
    _rate_limit_store[client_ip] = now
    return False


@main_bp.route("/api/health", methods=["GET"])
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Database health check failed.")
        return jsonify({"status": "unavailable", "database": "unavailable"}), 503
    return jsonify({"status": "ok", "database": "connected", "message": "Portfolio backend is healthy."}), 200


@main_bp.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify({"projects": get_projects_data()}), 200


@main_bp.route("/api/skills", methods=["GET"])
def get_skills():
    return jsonify({"skills": get_skills_data()}), 200


@main_bp.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    payload, error = validate_contact_payload(data)
    if error:
        return jsonify({"error": error}), 400

    client_ip = request.remote_addr or "unknown"
    if _is_rate_limited(client_ip):
        return jsonify({"error": "Too many contact attempts. Please wait a moment before sending another message."}), 429

    try:
        contact, error = save_contact_message(payload)
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Contact message could not be saved.")
        return jsonify({"error": "The message could not be saved. Please try again later."}), 500

    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Message sent successfully.", "contact_id": contact["id"]}), 201
