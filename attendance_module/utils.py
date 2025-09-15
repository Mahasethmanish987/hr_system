
from datetime import time
from django.utils import timezone
from datetime import datetime


def apply_check_in(attendance): 
    """
    Apply check-in rules like late arrival, early exit, etc.

    """
    from .models import Attendance
    if not attendance.check_in: 
        return 

    check_in_local = timezone.localtime(attendance.check_in)
    if check_in_local.time()>time(10,20): 
        attendance.late_arrival=True 
    else: 
        attendance.late_arrival=False 
    
        

def check_out_rules(attendance): 
      """Apply rules for the checkout"""
      from .models import Attendance

      if not attendance.check_out:
        return 
      check_out_local=timezone.localtime(attendance.check_out)
       
      if check_out_local.time()<time(17,40): 
          attendance.early_exit=True 
      else: 
          attendance.early_exit= False


def calculate_working_summary(attendance): 
    from .models import Attendance
    from attendance_module.models import WorkingSummary

    if not attendance.check_in  or not attendance.check_out:
        return None 
    check_in_dt = timezone.localtime(attendance.check_in)
    check_out_dt = timezone.localtime(attendance.check_out)

    worked_time = check_out_dt - check_in_dt
    worked_hours = worked_time.total_seconds() / 3600
    overtime_hours=0 

    total_hours=worked_hours + overtime_hours
    
    summary,created=WorkingSummary.objects.update_or_create(
        attendance=attendance, 
        defaults={
            'worked_hours': round(worked_hours,2),
            "overtime_hours":round(overtime_hours,2),
            "total_hours":round(total_hours,2)
        }
    )


              
def determine_status(attendance):
    """Determine status based on check-in/check-out and worked hours."""
    if not attendance.check_in:
        attendance.status = "absent"
        return

    if not attendance.check_out:
        attendance.status = "in-progress"
        return

    # Calculate worked hours
    check_in_dt = timezone.localtime(attendance.check_in)
    check_out_dt = timezone.localtime(attendance.check_out)
    worked_hours = (check_out_dt - check_in_dt).total_seconds() / 3600

    # Determine status based on worked hours
    if worked_hours <=3:
        attendance.status = "leave"
    elif worked_hours <=6:
        attendance.status = "half-day"
    else:
        attendance.status = "present"
    