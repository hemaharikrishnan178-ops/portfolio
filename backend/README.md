# Backend

See the root [README](../README.md) for full local setup, environment, database migration, API, test, and deployment instructions.

Run backend commands from this directory:

```powershell
.\.venv\Scripts\Activate.ps1
flask --app run db upgrade
flask --app run seed
python run.py
```

Run tests with `pytest`.
