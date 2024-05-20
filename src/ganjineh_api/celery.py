import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ganjineh_api.settings.local")

app = Celery("ganjineh_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
