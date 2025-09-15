import factory
from datetime import date 
from attendance_module.models import Attendance,OvertimeRate,OvertimeRequest,WorkingSummary
from employee_module.factories import EmployeeFactory


class AttendanceFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=Attendance

    employee=factory.SubFactory(EmployeeFactory)
    date=factory.LazyFunction(date.today) 
    status='in-progress'
    check_in=None 
    check_out=None 
    late_arrival=False 
    early_exit=False 



class OvertimeFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=OvertimeRequest
    
    employee=factory.SubFactory(EmployeeFactory)
    attendance=factory.SubFactory(AttendanceFactory)
    requested_hour=0 
    status='pending'
    
    approval_date=None 
    approved_by=factory.SubFactory(EmployeeFactory)    


class OvertimeRateFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=OvertimeRate
    employee=factory.SubFactory(EmployeeFactory)
    overtime_rate=0
