"""
Django settings for RedNet project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['DJANGO_SECRET_REDNET']

# В продакшне выставить PRODUCTION=True
IS_PRODUCTION = os.environ.get('PRODUCTION', 'False') == 'True'
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ── Security ──────────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT          = IS_PRODUCTION
SESSION_COOKIE_SECURE        = IS_PRODUCTION
CSRF_COOKIE_SECURE           = IS_PRODUCTION
SESSION_COOKIE_HTTPONLY      = True
CSRF_COOKIE_HTTPONLY         = True
X_FRAME_OPTIONS              = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF  = True
SECURE_HSTS_SECONDS          = 31536000 if IS_PRODUCTION else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_PRODUCTION
SECURE_HSTS_PRELOAD          = IS_PRODUCTION


# ── Apps ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'about.apps.AboutConfig',
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RedNet.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'RedNet/templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'RedNet.wsgi.application'


# ── Database ──────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ── Auth ──────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ── i18n ──────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL   = 'static/'
STATIC_ROOT  = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'RedNet/templates/css',
    BASE_DIR / 'RedNet/templates/fonts',
    BASE_DIR / 'RedNet/templates/js',
    BASE_DIR / 'RedNet/templates/img',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
