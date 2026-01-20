from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
from .api_services import fetch_all_data

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Her 10 dakikada bir tüm API'leri tara
    scheduler.add_job(fetch_all_data, 'interval', minutes=10, id='master_job', replace_existing=True)

    try:
        scheduler.start()
        print("Scheduler Başladı!")
    except Exception as e:
        print(e)