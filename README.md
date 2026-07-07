# API Deployment Project

Flask API project configured with SQLAlchemy and Flask-Migrate, prepared for local development and Render deployment.

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic
- Gunicorn

## Project Structure

- `flask_app.py`: Application entrypoint
- `app/`: App package (factory, config, extensions, models)
- `migrations/`: Alembic migration repository
- `requirements.txt`: Python dependencies

## Local Setup

1. Create and activate virtual environment:

```powershell
py -3 -m venv venv
. .\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run database migrations:

```powershell
python -m flask --app flask_app db upgrade
```

4. Start the app:

```powershell
python flask_app.py
```

The app runs on http://127.0.0.1:5000 by default.

## Migration Commands

Create a migration after model changes:

```powershell
python -m flask --app flask_app db migrate -m "Describe changes"
```

Apply migrations:

```powershell
python -m flask --app flask_app db upgrade
```

## Render Deployment Notes

- App binds with `host=0.0.0.0`
- Port is read from the `PORT` environment variable
- Set `DATABASE_URI` in Render environment variables
- Set `SECRET_KEY` in Render environment variables

## Remote Repository

GitHub: https://github.com/dbeltran16/API-Deployment-Project
