import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail_future_me.settings")

app = Celery(__name__)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
