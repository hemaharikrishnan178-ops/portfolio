# Full-Stack Personal Portfolio Website

Portfolio website for the Thiranex internship assignment. It presents Hema H's profile, skills, learning-focused experience, and exactly two portfolio projects: **TrustShare** and **Uzhavan AI**.

- **GitHub:** [hemaharikrishnan178-ops/portfolio](https://github.com/hemaharikrishnan178-ops/portfolio)
- **Live website:** Not deployed yet.

## Features

- Responsive React portfolio with About, Education, Skills, Projects, Experience, and Contact sections.
- Project and skill content loaded from the Flask API.
- Exactly two seeded portfolio projects: TrustShare and Uzhavan AI.
- Project detail modal without unverified repository or demo links.
- Contact form validation, API persistence, and basic per-process rate limiting.
- Resume download from `frontend/public/Hema_H_Resume.pdf`.
- Flask API backed by SQLite for local development and PostgreSQL for production.
- Health endpoint reports database connectivity.

## Technology stack

- Frontend: React, Vite, JavaScript, CSS
- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Migrate
- Database: SQLite locally; PostgreSQL with Psycopg 3 in production

## Architecture

```text
Browser
  ├── React/Vite frontend ── GET /api/projects, GET /api/skills, POST /api/contact ──┐
  │                                                                                │
  └── Resume PDF served as a frontend public asset                                 ▼
                                                                    Flask API
                                                                        │
                                                         SQLAlchemy / Flask-Migrate
                                                                        │
                                                      SQLite (local) / PostgreSQL (production)
```

## Project structure

```text
backend/
  app/
    config/       Environment-based application settings
    models/       Project, skill, and contact message models
    routes/       Health, project, skill, and contact API endpoints
    services/     Seed data and contact/project services
  migrations/     Database migration documentation
  tests/          Backend API and persistence tests
  requirements.txt
  run.py
frontend/
  public/         Resume and public static assets
  src/            React application and styles
  package.json
  vite.config.js
```

## Local installation

Requirements: Node.js (compatible with the Vite version in `frontend/package-lock.json`) and Python 3.12 or newer.

1. Clone the repository and open a terminal in its root.
2. Create and activate the backend virtual environment:

   ```powershell
   cd backend
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

3. Keep the example's local SQLite configuration for development. Initialize the schema and seed the two portfolio projects and skills:

   ```powershell
   flask --app run db upgrade
   flask --app run seed
   ```

4. Start the API:

   ```powershell
   python run.py
   ```

   The backend listens at `http://localhost:5000`.

5. In a second terminal, start the frontend:

   ```powershell
   cd frontend
   npm ci
   Copy-Item .env.example .env
   npm run dev
   ```

   Open the local URL printed by Vite (normally `http://localhost:5173`).

## Environment variables

Backend variables belong in the untracked `backend/.env` file. Configure them in the hosting provider's secret/environment settings for deployment.

| Variable | Purpose | Local example |
|---|---|---|
| `APP_ENV` | `development` or `production` | `development` |
| `SECRET_KEY` | Flask signing key; use a generated secret in production | Local-only placeholder in `.env.example` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///instance/hema_portfolio.db` |
| `FRONTEND_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `CONTACT_RATE_LIMIT_SECONDS` | Minimum interval between accepted submissions from one IP per backend process | `30` |
| `VITE_API_URL` | Backend base URL compiled into the frontend; leave empty locally | Empty locally; set to backend HTTPS URL in production |

For local development, Vite proxies `/api` requests to the Flask server at `127.0.0.1:5000`. For production, set `APP_ENV=production`, a private `SECRET_KEY`, a PostgreSQL `DATABASE_URL` using the `postgresql+psycopg://` scheme, and `FRONTEND_ORIGINS` to the exact deployed HTTPS frontend origin. Set `VITE_API_URL` to the backend HTTPS base URL as a frontend build variable. It is public configuration, not a secret. Never put database credentials or secret keys in frontend variables.

## Database setup and migrations

SQLite is used locally. The repository includes a Flask-Migrate baseline revision. Run migration commands from the backend directory:

```powershell
flask --app run db upgrade
```

To create future revisions, run `flask --app run db migrate -m "Describe schema change"` and review the generated migration before applying it. Run `flask --app run seed` after the initial upgrade and whenever seeded portfolio data needs synchronization. For production, run migrations and the seed command as a release step before starting the web service.

## API

All endpoints are served by the Flask backend.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/health` | Backend/database health; returns HTTP 503 if the database is unavailable |
| `GET` | `/api/projects` | Returns exactly the TrustShare and Uzhavan AI project records |
| `GET` | `/api/skills` | Returns database-backed skill records |
| `POST` | `/api/contact` | Validates and saves a contact message |

Example contact request:

```json
{
  "name": "Example Visitor",
  "email": "visitor@example.com",
  "subject": "Project inquiry",
  "message": "I would like to discuss your portfolio."
}
```

Successful submissions return HTTP `201`; invalid fields return `400`; repeated accepted submissions within the configured interval return `429`. Messages are stored in the `contact_messages` table. Do not submit real personal details when testing.

## Tests and frontend checks

From the repository root:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

In a separate terminal:

```powershell
cd frontend
npm ci
npm run lint
npm run build
```

## Deployment

`vercel.json` configures one Vercel project with two services: the Flask API under `/api/*` and the Vite frontend for the remaining paths. Both are served from the same HTTPS origin, so the frontend uses relative API URLs and does not need a public backend URL variable.

1. Import this GitHub repository into Vercel and keep the repository root as the project root so it can discover `vercel.json`.
2. Configure the backend service environment variables in Vercel: `APP_ENV=production`, `SECRET_KEY`, `DATABASE_URL`, and `FRONTEND_ORIGINS` (the deployed site origin).
3. Provision a persistent PostgreSQL database and set `DATABASE_URL` to its private connection string using the `postgresql+psycopg://` scheme. Do not use local SQLite for serverless production.
4. Apply `flask --app run db upgrade` and `flask --app run seed` from the backend service before the first public use and after schema updates.
5. Deploy, then verify `/api/health`, both project records, skills, contact persistence, the PDF download, refresh behavior, and HTTPS.

Never put backend secrets in `VITE_*` environment variables or commit them. The deployment is not complete until the project and database have been provisioned and the live API checks pass.

## Known limitations and remaining setup

- The GitHub repository is public; the live website is not deployed yet.
- The TrustShare GitHub repository URL and demo URLs are intentionally omitted until verified.
- Contact rate limiting is in-memory and per backend process; use shared persistent rate limiting if scaling across multiple workers.
- Schema changes should use reviewed Flask-Migrate revisions.
- The Education section points to the resume rather than repeating academic details.
