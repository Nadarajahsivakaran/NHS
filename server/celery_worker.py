from celery import Celery

celery = Celery(
    'app',
    broker='redis://localhost:6379/0',  # Redis broker URL, update if needed
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
