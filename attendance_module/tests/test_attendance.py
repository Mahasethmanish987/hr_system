import pytest 
from datetime import date 
from attendance_module.models import Attendance
from payroll_module.utils import count_working_days
from django.db.models import Sum 
from attendance_module.services.attendance_services import AttendanceService

def test_attendance_creation(db,test_employee,leave_request_conftest,create_attendance_for_month): 
    starting_date=date(2025,8,1)
    ending_date=date(2025,8,31)
    attendance_records=Attendance.objects.filter(employee=test_employee,date__range=[starting_date,ending_date])
   
    assert len(attendance_records)==count_working_days(starting_date)

def test_attendance_creation_with_overtime(db,test_employee,leave_request_conftest,attendance_with_overtime):      
    starting_date=date(2025,8,1)
    ending_date=date(2025,8,31)
    overtime_hours=Attendance.objects.filter(employee=test_employee,date__range=[starting_date,ending_date]).aggregate(total=Sum('working_summary__overtime_hours'))['total']
    assert overtime_hours==10


def test_calculate_present_absent_leave_half_day_overtime(db,test_employee,leave_request_conftest,attendance_with_overtime): 
    starting_date=date(2025,8,1)
    ending_date=date(2025,8,31)
    attendance_details=AttendanceService.get_attendance_datail_by_month(test_employee.id,starting_date,ending_date)

    assert attendance_details['half_day']==2
    assert attendance_details['leave']==4
    assert attendance_details['absent']==2
    assert attendance_details['present_day']==18
    assert attendance_details['overtime_hours']==10


 