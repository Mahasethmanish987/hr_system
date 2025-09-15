from celery import shared_task
from django.utils import timezone
from employee_module.models import Employee
from datetime import time, datetime
from .models import Attendance
import logging 
from leave_module.services.leave_services import LeaveRequestService
from attendance_module.services.attendance_services import AttendanceService

logger = logging.getLogger(__name__)
@shared_task(name="created_daily_attendance")
def create_daily_attendance():
    today = timezone.localdate()
    AttendanceService.initialize_attendance_records_for_date(date=today)
    



@shared_task(name="check_check_out")
def check_check_out():
    today = timezone.localdate()

    absent_attendance = AttendanceService.retrieve_attendance(date=today, check_in_isnull=True)
    for attendance in absent_attendance:
        if LeaveRequestService.check_leave_approval(attendance.employee.id,today):
            
            status={'status':'leave'}
        else:
          
          status={'status':'absent'}
        AttendanceService.update_attendance(attendance.id,status)

    forget_checkout_attendance = AttendanceService.retrieve_attendance(
        date=today, check_in_isnull=False, check_out_isnull=True
    )
    six_pm = datetime.combine(today, time(18, 0))
    six_pm = timezone.make_aware(six_pm, timezone.get_current_timezone())
    for attendance in forget_checkout_attendance:
        check_out={'check_out':six_pm}
        AttendanceService.update_attendance(attendance.id,check_out)
        
        