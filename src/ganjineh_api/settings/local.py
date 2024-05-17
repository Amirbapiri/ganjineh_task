from .base import *
from .base import env


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="afzgTWz3XpqzPcLwd+J7PjkH4pID08CkbUNUbsXa//Ax61yqac9CPg==",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://0.0.0.0:8080"]

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = ["0.0.0.0"]
