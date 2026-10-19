from app.extensions import db
from app.models.project import Project
from app.models.skill import Skill


def get_skills_data():
    return [skill.to_dict() for skill in Skill.query.order_by(Skill.category.asc(), Skill.name.asc()).all()]


def seed_database():
    project_data = [
        {
            "title": "TrustShare — Secure File-Sharing Platform",
            "slug": "trustshare",
            "category": "Full-Stack Development | Cybersecurity",
            "description": "TrustShare is a secure file-sharing platform designed to let users upload, store, and share files through authenticated and controlled access mechanisms.",
            "technologies": "Next.js, React, TypeScript, Python, FastAPI, SQLAlchemy, JWT authentication, Docker, PostgreSQL, Cloud Storage",
            "status": "featured",
            "repository_url": None,
            "demo_url": None,
        },
        {
            "title": "Uzhavan AI — Intelligent Farming Companion",
            "slug": "uzhavan-ai",
            "category": "Artificial Intelligence | Agriculture | Sustainability",
            "description": "Uzhavan AI is an intelligent farming solution concept explored during ISTE Hackathon 2026 in the Water and Agriculture track. It focuses on combining agricultural information, weather, soil, and market insights to support better farming decisions.",
            "technologies": "Python, Machine Learning, NLP, Image Classification, Recommendation Systems, Predictive Analytics",
            "status": "featured",
            "repository_url": None,
            "demo_url": None,
        },
    ]

    for item in project_data:
        project = Project.query.filter_by(slug=item["slug"]).first()
        if project:
            for key, value in item.items():
                setattr(project, key, value)
        else:
            db.session.add(Project(**item))

    skill_data = [
        ("Python", "Programming", "Basic/Intermediate"),
        ("C", "Programming", "Basic"),
        ("Java", "Programming", "Currently Learning"),
        ("HTML", "Frontend", "Core markup and structure"),
        ("CSS", "Frontend", "Responsive styling and layout"),
        ("JavaScript", "Frontend", "Basics"),
        ("React.js", "Frontend", "Basics"),
        ("Python backend development", "Backend and databases", "API and backend logic"),
        ("REST APIs", "Backend and databases", "Data exchange between frontend and backend"),
        ("MongoDB", "Backend and databases", "Basics"),
        ("DBMS", "Backend and databases", "Database fundamentals"),
        ("Git", "Tools", "Version control"),
        ("GitHub", "Tools", "Code hosting and collaboration"),
        ("VS Code", "Tools", "Development environment"),
        ("Postman", "Tools", "API testing"),
        ("Linux", "Tools", "Basics"),
        ("Object-Oriented Programming", "Core concepts", "Designing reusable code"),
        ("Data Structures and Algorithms", "Core concepts", "Currently Practicing"),
        ("AI application development", "Core concepts", "AI-driven solutions"),
        ("Prompt engineering basics", "Core concepts", "Effective AI prompt design"),
    ]

    for name, category, proficiency in skill_data:
        if not Skill.query.filter_by(name=name, category=category).first():
            db.session.add(Skill(name=name, category=category, proficiency_description=proficiency))

    db.session.commit()
