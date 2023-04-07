from celery import shared_task
from .views import daily_quote


@shared_task
def my_daily_task():
    daily_quote()
