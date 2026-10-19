import re

from app.extensions import db
from app.models.contact_message import ContactMessage


def validate_contact_payload(data):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."

    fields = ("name", "email", "subject", "message")
    if any(not isinstance(data.get(field), str) for field in fields):
        return None, "All fields must be text."

    name = data["name"].strip()
    email = data["email"].strip()
    subject = data["subject"].strip()
    message = data["message"].strip()

    if not all([name, email, subject, message]):
        return None, "All fields are required."

    if len(name) > 100 or len(email) > 150 or len(subject) > 150 or len(message) > 1200:
        return None, "One or more fields exceed the maximum length."

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return None, "Please enter a valid email address."

    return {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }, None


def save_contact_message(data):
    payload, error = validate_contact_payload(data)
    if error:
        return None, error

    contact = ContactMessage(**payload)
    db.session.add(contact)
    db.session.commit()
    return contact.to_dict(), None
