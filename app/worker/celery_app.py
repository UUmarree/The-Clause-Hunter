#config file that connects celery to redis
from celery import Celery
from app.core.config import settings

celery_task_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_task_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    imports=["app.worker.tasks"],
)