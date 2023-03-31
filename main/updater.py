from apscheduler.schedulers.background import BackgroundScheduler
from main.main_job import main_job


def start():
    print("FROM MAIN CATALOGUE")
    scheduler = BackgroundScheduler()
    # scheduler.add_job(main_job, 'interval', seconds=15, replace_existing=True)
    scheduler.add_job(main_job, 'cron', hour=0, minute=23, second=5, replace_existing=True)
    scheduler.start()
