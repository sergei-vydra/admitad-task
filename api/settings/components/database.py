from api import settings

DATABASES = {
    "default": {
        **settings.env.db(),
        "CONN_HEALTH_CHECKS": True,
        "CONN_MAX_AGE": settings.env.int("DB_CONN_MAX_AGE", default=0),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
