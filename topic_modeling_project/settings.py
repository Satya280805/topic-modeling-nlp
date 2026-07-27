"""
Django settings for topic_modeling_project.
"""

from pathlib import Path
import os

# ─────────────────────────────────────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────────────────────────────────────
# Build paths inside the project like: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────
# IMPORTANT: Keep this secret in production. Never expose it publicly.
SECRET_KEY = 'django-insecure-topic-modeling-secret-key-change-in-production'

# DEBUG = True means detailed error pages are shown. Set to False in production.
DEBUG = True

# Hosts/domains allowed to serve this Django site.
ALLOWED_HOSTS = ['*']


# ─────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────────────────────────────────────
# Django built-in apps + our custom app 'topic_app'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'topic_app',                  # ← Our custom application
]

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Protects forms from CSRF attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─────────────────────────────────────────────────────────────────────────────
# URL CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
ROOT_URLCONF = 'topic_modeling_project.urls'

# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look for templates inside each app's 'templates' folder
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'topic_modeling_project.wsgi.application'

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────────────────
# We use SQLite (a simple file-based DB). Good for development.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# STATIC FILES (CSS, JavaScript, Images)
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'

# ─────────────────────────────────────────────────────────────────────────────
# MEDIA FILES (User Uploads)
# ─────────────────────────────────────────────────────────────────────────────
# MEDIA_ROOT: folder on disk where uploaded files are saved
MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL: URL prefix used to access uploaded files via browser
MEDIA_URL = '/media/'

# ─────────────────────────────────────────────────────────────────────────────
# FILE UPLOAD SETTINGS
# ─────────────────────────────────────────────────────────────────────────────
# Maximum upload size = 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT AUTO FIELD
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE & TIMEZONE
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
