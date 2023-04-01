from apscheduler.schedulers.background import BackgroundScheduler
from main.main_job import main_job


def start():
    print("FROM MAIN CATALOGUE")
    scheduler = BackgroundScheduler()
    scheduler.add_job(main_job, 'cron', second=10, replace_existing=True)
    scheduler.start()
