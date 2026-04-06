# BAIUST Robotics Society (BARS) - Django Project

This README is prepared for IT Wing deployment and local setup.

## 1. Project Overview

This is a Django web application for BARS with:
- Main Django project: `BARS`
- Main app: `VP`
- Database (default): SQLite (`db.sqlite3`)
- Static files: `static/` and `staticfiles/`
- Media uploads: `media/`

## 2. Current Python Dependencies

Dependencies are managed from `requirements.txt`:
- Django==4.2.0
- Pillow==10.0.0
- python-decouple==3.8

Install them with:

```bash
pip install -r requirements.txt
```

## 3. Prerequisites

- Python 3.10+ (recommended)
- pip (comes with Python)
- Git (optional, for pulling source)

## 4. Setup on Windows

Run these commands in PowerShell from project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## OR Setup on Linux

Run these commands from project root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Open: `http://127.0.0.1:8000/` (or server IP if remote)

## 5. Development Mode

Use Django development server:

```bash
python manage.py runserver
```

Notes:
- Hot reload is enabled.
- Suitable for local development/testing only.

## 6. Production Mode (Recommended Guidance)

Important: Current `BARS/settings.py` has `DEBUG = True`, hardcoded `SECRET_KEY`, and SQLite. These are not recommended for production.

### 6.1 Minimum Production Changes

IT Wing should create a production settings strategy (for example `BARS/settings_prod.py`) or environment-based config.

Minimum requirements:
- `DEBUG = False`
- Set secure `SECRET_KEY` from environment variable
- Set `ALLOWED_HOSTS` to real domain/IP
- Keep email/app secrets out of source code
- Use a production database (PostgreSQL/MySQL) instead of SQLite for multi-user reliability
- Serve static files via Nginx/Apache/CDN

### 6.2 Production Server on Linux (Typical)

Install additional production packages:

```bash
pip install gunicorn whitenoise
```

Run app with Gunicorn:

```bash
gunicorn BARS.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Typical stack:
- Nginx (reverse proxy + static/media)
- Gunicorn (WSGI app server)
- systemd (process manager)

### 6.3 Production Server on Windows (If Needed)

Gunicorn does not officially support Windows. Use Waitress:

```powershell
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 BARS.wsgi:application
```

## 7. Useful Management Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py check --deploy
```

## 8. Deployment Checklist for IT Wing

- Python and virtual environment created
- Dependencies installed from `requirements.txt`
- Migrations applied
- Static files collected
- Superuser created
- `DEBUG=False` in production
- `ALLOWED_HOSTS` configured
- Secret keys and email credentials moved to environment variables
- Production app server configured (Gunicorn on Linux / Waitress on Windows)
- Reverse proxy configured (Nginx/Apache)

## 9. Quick Start Summary

### Windows (development)

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Linux (development)

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

---
Prepared for BARS IT Wing. If needed, I can also provide a ready-to-use `settings_prod.py`, `.env.example`, and a sample Nginx + systemd configuration.
