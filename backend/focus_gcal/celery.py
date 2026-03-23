import os

from celery import Celery, Task


class GlobalRetryTask(Task):
    autoretry_for = (Exception,)
    retry_backoff = 5
    retry_jitter = False
    retry_kwargs = {"max_retries": 3}


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "focus_gcal.settings")

app = Celery("focus_gcal", task_cls=GlobalRetryTask)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
