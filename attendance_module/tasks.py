from celery import shared_task
from django.utils import timezone
from employee_module.models import Employee
from datetime import time, datetime
from .models import Attendance


@shared_task(name="created_daily_attendance")
def create_daily_attendance():
    today = timezone.localdate()
    active_employees = Employee.objects.filter(is_active=True)
    created_count = 0

    for employee in active_employees:
        try:
            obj, created = Attendance.objects.get_or_create(
                employee=employee, date=today
            )
            if created:
                created_count += 1
        except Exception as e:
            print(f"Failed for {employee.employee_code}: {e}")

    print(f"Attendance created for {created_count} employees")


@shared_task(name="check_check_out")
def check_check_out():
    today = timezone.localdate()

    absent_attendance = Attendance.objects.filter(date=today, check_in__isnull=True)
    for attendance in absent_attendance:
        attendance.status = "absent"
        attendance.save()

    forget_checkout_attendance = Attendance.objects.filter(
        date=today, check_in__isnull=False, check_out__isnull=True
    )
    six_pm = datetime.combine(today, time(18, 0))
    six_pm = timezone.make_aware(six_pm, timezone.get_current_timezone())
    for attendance in forget_checkout_attendance:
        attendance.check_out = six_pm
        attendance.save()
        