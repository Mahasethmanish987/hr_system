from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
from decouple import config
# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-default-key")
DEBUG = True
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1").split(",")

# INSTALLED APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "employee_module",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "task",
    "attendance_module",
    "django_celery_results",
    "django_celery_beat",
    "leave_module",
    "drf_spectacular_sidecar",
    "drf_spectacular",
]

# MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# DATABASE
DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://postgres_database_gp67_user:4U3if7BMLF9LKVRKuhcmHkcp3bGsoASL@dpg-d2m89gggjchc73f6fe00-a.oregon-postgres.render.com:5432/postgres_database_gp67"
    )
}
# AUTH PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# STATIC AND MEDIA
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

# CELERY
CELERY_BROKER_URL = config("REDIS_URL")
print(CELERY_BROKER_URL)
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_ENABLE_UTC = True
CELERY_TASK_RESULT_EXPIRES = 3600


CSRF_TRUSTED_ORIGINS = [
    "https://hr-system-10.onrender.com",  # must match exactly with the URL in browser
    "http://localhost:5173",              # your Vue app
]

CORS_ALLOWED_ORIGINS = [
    "https://hr-system-10.onrender.com",
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True   