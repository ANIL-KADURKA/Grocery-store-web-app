# celery_config.py

from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


CELERY_BEAT_SCHEDULE = {
    'generate-monthly-report': {
        'task': 'tasks.generate_monthly_report',
        'schedule': crontab(day_of_month='1'),
    },
}

# Configure Celery Beat schedule
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE