from celery import Celery
from config import config

celery_app = Celery(
    "worker",
    broker=config.redis.redis_url,
    backend=config.redis.redis_url,
    include=[
        "app.utils.tasks.bitrix_task"
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_expires=3600,
)