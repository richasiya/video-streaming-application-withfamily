# withfamily

Media streaming platform(withfamily) built with Django. It supports movies, web series, short films, and podcasts, with user profiles, watch history, and a subscription model (free/basic/premium). Payments are integrated via Razorpay.

## Features
- Content library with categories and access levels
- Watch page with related content suggestions
- User accounts, profiles, watchlist, and watch history
- Subscription plans with Razorpay checkout
- Admin panel for managing content

## Tech Stack
- Django
- SQLite (development)
- Razorpay

## Project Structure
- `myproject/` Django project settings, URLs, WSGI/ASGI
- `content/` Content models, views, templates
- `users/` User profiles, authentication, watchlist/history
- `static/` Static assets and CSS
- `media/` Uploaded thumbnails and videos

## Setup

### 1) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Run migrations
```powershell
python manage.py migrate
```

### 4) Create a superuser (optional)
```powershell
python manage.py createsuperuser
```

### 5) Run the server
```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Environment Variables
These are optional in development. If not set, defaults in `myproject/settings.py` are used.

- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

## Production Notes
Production settings are in `settings_production.py` and include:
- `python-dotenv` for environment variables
- `dj-database-url` for `DATABASE_URL`
- `whitenoise` for static file serving

Set these environment variables in production:
- `SECRET_KEY`
- `DEBUG` (`True`/`False`)
- `ALLOWED_HOSTS` (comma-separated)
- `DATABASE_URL`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

## License
Private project. Add a license if you plan to share publicly.
