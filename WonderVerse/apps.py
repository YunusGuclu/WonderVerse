from django.apps import AppConfig

class ÇocukConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Çocuk'

    def ready(self):
        from . import tasks
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJobStore
        import sys

        if 'runserver' not in sys.argv:
            return

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(tasks.gorev_pokemon_avla, 'interval', seconds=45, id='poke', replace_existing=True)
        scheduler.add_job(tasks.gorev_uzay_istasyonu, 'interval', hours=1, id='space', replace_existing=True)
        scheduler.add_job(tasks.gorev_heroes, 'interval', minutes=2, id='craft', replace_existing=True)
        scheduler.add_job(tasks.gorev_sanat, 'interval', minutes=3, id='art', replace_existing=True)
        scheduler.add_job(tasks.gorev_hayvan_saka, 'interval', seconds=50, id='mix', replace_existing=True)
        scheduler.add_job(tasks.gorev_minik_sef, 'interval', hours=4, id='chef', replace_existing=True)
        try:
            scheduler.start()
            print(">>> ÇOCUK PORTALI SİSTEMLERİ AKTİF EDİLDİ <<<")
        except: pass