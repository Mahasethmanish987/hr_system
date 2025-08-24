import os 
from celery import Celery 
from celery.schedules import crontab 
os.environ.setdefault("DJANGO_SETTINGS_MODULE","mysite.settings")


app=Celery("mysite")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule={
    "created_daily_attendance":{
    "task":"created_daily_attendance",
    "schedule": crontab(hour=11,minute=45),
    "args":(),
    },
    "check_check_out": {
        "task": "check_check_out",       # your Celery task name
        "schedule": crontab(hour=15, minute=52),  # 6:30 PM daily
        "args": (),
    },
}


