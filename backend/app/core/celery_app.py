import platform
from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "whatsapp_automation_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,  # <-- Fix warning
)

# Autodiscover current task folder properly
celery_app.autodiscover_tasks(["app.tasks"])

# Force-load task module to prevent lazy loading issues
import app.tasks.whatsapp_tasks

# Windows fix (prefork not supported)
if platform.system() == "Windows":
    celery_app.conf.worker_pool = "solo"
