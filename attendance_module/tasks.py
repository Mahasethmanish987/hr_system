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

    existing_employee_ids=Attendance.objects.filter(date=today).values_list('employee_id', flat=True)

    missing_employees=active_employees.exclude(id__in=existing_employee_ids)

    attendance_to_create=[Attendance(employee=emp,date=today) for emp in missing_employees]
    Attendance.objects.bulk_create(attendance_to_create)
    print(f"created attendance for {len(attendance_to_create)}")

    
def check_leave(employee,date)->bool: 
    from leave_module.models import LeaveRequest
    leave=LeaveRequest.objects.filter(
        employee=employee,
        start_date__lte=date,
        end_date__gte=date,
        status="approved"
    ).exists()
    return leave



@shared_task(name="check_check_out")
def check_check_out():
    today = timezone.localdate()

    absent_attendance = Attendance.objects.filter(date=today, check_in__isnull=True)
    for attendance in absent_attendance:
        if check_leave(attendance.employee,today):
            attendance.status = "leave"
        else:
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
        