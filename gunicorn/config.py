from api.settings import env

GUNICORN_WORKERS = env.int("GUNICORN_WORKERS", default=4)

bind = "0.0.0.0:9996"
workers = GUNICORN_WORKERS
