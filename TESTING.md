# Local Testing Guide (app_appel)

## 1. Virtual Environment & Dependencies
- Use Django 5.2.* (Django 6.0.3 pinned in requirements.txt does not exist on PyPI).
- Installation:
  python3 -m venv .venv
  .venv/bin/pip install "Django==5.2.*" dj-database-url python-dotenv reportlab whitenoise gunicorn

## 2. Environment Variables & Setup
Always pass environment variables inline for local commands:
- Migrate: `SECRET_KEY=test DEBUG=True .venv/bin/python manage.py migrate`
- Seed Data: `SECRET_KEY=test DEBUG=True .venv/bin/python manage.py setup_data`
- Run Server: `SECRET_KEY=test DEBUG=True .venv/bin/python manage.py runserver 0.0.0.0:8000`
- Run Tests: `SECRET_KEY=test .venv/bin/python manage.py test`

## 3. Important Gotchas
- **School Names:** Formulars enforce exact matching from `Ecole.nom` created by `setup_data`. Enter full names (e.g., `École Nationale Supérieure des Travaux Publics`), not abbreviations (`ENSTP`).
- **Student GPS Validation:** On the student dashboard, pressing **Enter** inside the code field submits the form without triggering desktop browser GPS blocks.
- **Forgot Password:** Requires real Gmail SMTP credentials in environment variables; otherwise, the mail delivery fails gracefully.