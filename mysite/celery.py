import os 
from celery import Celery 
from celery.schedules import crontab 
os.environ.setdefault("DJANGO_SETTINGS_MODULE","mysite.settings.settings")


app=Celery("mysite")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule={
    "created_daily_attendance":{
    "task":"created_daily_attendance",
    "schedule": crontab(hour=14,minute=26),
    "args":(),
    },
    "check_check_out": {
        "task": "check_check_out",      
        "schedule": crontab(hour=14, minute=30),  
        "args": (),
    },
    "calculate_salary_monthly": {
        "task": "calculate_salary",      
        "schedule": crontab(hour=0, minute=0, day_of_month=2),  
        "args": (),
    },
}


