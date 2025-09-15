import factory 
from datetime import date ,timedelta
from employee_module.factories import EmployeeFactory
from .models import LeaveBalance,LeaveRequest

class LeaveRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaveRequest

    employee = factory.SubFactory(EmployeeFactory)
    leave_type = factory.Iterator(["casual", "sick"])
    start_date = factory.LazyFunction(lambda: date.today())
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=1))
    reason = factory.Faker("sentence")
    status = "pending"
    approved_by = None
    approved_date = None

class LeaveBalanceFactory(factory.django.DjangoModelFactory): 

    class Meta: 
        model=LeaveBalance

    employee= factory.SubFactory(EmployeeFactory)
    month=None 
    casual_leaves=1
    sick_leaves= 0    
