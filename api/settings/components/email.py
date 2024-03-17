from api.settings import env

EMAIL_HOST = env("EMAIL_HOST", default=None)
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS: bool = env("EMAIL_USE_TLS")
EMAIL_USE_SSL: bool = env("EMAIL_USE_SSL")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if not EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
