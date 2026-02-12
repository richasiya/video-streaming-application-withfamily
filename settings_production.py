import os
from pathlib import Path
from .settings import *  # import base settings

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Database: prefer DATABASE_URL (Postgres) in production
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'))
}

# Static files with WhiteNoise
MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security recommendations
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Gunicorn will bind to PORT

# Razorpay secrets (override in production)
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', RAZORPAY_KEY_ID)
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', RAZORPAY_KEY_SECRET)
