import os
import sentry_sdk
import environ

env: environ.Env = environ.Env(
    ENV_FILE=(str, None),
    DEBUG=bool,
    TEST=bool,
    CELERY_REDIS_MAX_CONNECTIONS=int,
    CELERY_BROKER_POOL_LIMIT=int,
    CELERY_TASK_EAGER=bool,
    EMAIL_HOST_PASSWORD=str,
    EMAIL_USE_TLS=bool,
    EMAIL_USE_SSL=bool,
)
ENV_FILE: str = env.str("ENV_FILE", default=".env")
env.read_env(ENV_FILE, overwrite=True)

# root
BASE_DIR: environ.Path = environ.Path(__file__) - 3
ROOT_URLCONF: str = "api.urls"
WSGI_APPLICATION: str = "api.wsgi.application"
ASGI_APPLICATION: str = "api.asgi.application"
SITE_NAME: str = env.str("SITE_NAME")

# django
SECRET_KEY: str = env("SECRET_KEY")
USE_BROWSABLE_API: bool = env.bool("USE_BROWSABLE_API")
DEBUG: bool = env("DEBUG")
TEST: bool = env("TEST")

sentry_sdk.init(
    dsn=env("SENTRY_URL"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

INSTALLED_APPS: list = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    # third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django_celery_beat",
    "django_filters",
    "drf_spectacular",
    # own apps
    "app.base",
    "app.users",
    "app.reminders",
]

MIDDLEWARE: list = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

TEMPLATES: list[dict[str, str | bool | dict | list]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ALLOWED_HOSTS: list = ["*"]
CORS_ALLOW_ALL_ORIGINS: bool = True
CORS_ALLOWED_ORIGINS: list = []
CSRF_TRUSTED_ORIGINS: list = ["http://localhost:*"]
SITE_ID: int = 1
INTERNAL_IPS: list = ["127.0.0.1", "0.0.0.0"]

STATIC_URL: str = "/static/"
STATIC_ROOT: str = BASE_DIR + "static"
MEDIA_URL: str = "/media/"
MEDIA_ROOT: str = BASE_DIR + "media"

USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True

TIME_ZONE: str = "UTC"
