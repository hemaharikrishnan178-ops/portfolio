from app.models.project import Project


def get_projects_data():
    required_slugs = ("trustshare", "uzhavan-ai")
    projects = Project.query.filter(Project.slug.in_(required_slugs)).all()
    projects_by_slug = {project.slug: project for project in projects}
    return [
        projects_by_slug[slug].to_dict()
        for slug in required_slugs
        if slug in projects_by_slug
    ]
