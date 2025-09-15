import pytest 
import datetime 
from pytest_factoryboy import register
from leave_module.factories import LeaveBalanceFactory, LeaveRequestFactory
from attendance_module.factories import AttendanceFactory, OvertimeFactory, OvertimeRateFactory
from employee_module.factories import EmployeeFactory, DepartmentFactory, JobTitleFactory, EmployeeStatusFactory, EmployeeTypeFactory, UserFactory
from leave_module.services.leave_services import LeaveRequestService
from employee_module.models import Employee
from datetime import date 
from django.utils import timezone
from payroll_module.factories import DeductionFactory,AllowanceFactory,TaxFactory,AllowanceChoices,TaxType,DeductionChoices

# Factory registrations
register(UserFactory)
register(EmployeeFactory)
register(EmployeeStatusFactory)
register(EmployeeTypeFactory)
register(DepartmentFactory)
register(JobTitleFactory)
register(AttendanceFactory)
register(OvertimeFactory)
register(LeaveBalanceFactory)
register(LeaveRequestFactory)
register(OvertimeRateFactory)
register(AllowanceFactory)
register(TaxFactory)
register(DeductionFactory)


@pytest.fixture
def test_employee(db):

   
        employee = EmployeeFactory()
        
        return employee

@pytest.fixture
def test_hr(db):
    
    
        employee = EmployeeFactory(role=Employee.HR)
       
        return employee

@pytest.fixture
def leave_balance_conftest(db, test_employee):
    
   
        balance_date = date(2025, 8, 1)
        leave_balance = LeaveBalanceFactory.create(
            employee=test_employee,
            casual_leaves=2,
            sick_leaves=2,
            month=balance_date
        )
        
        return leave_balance

@pytest.fixture
def leave_request_conftest(db, test_employee, test_hr):
    
        # First leave request
        start_date = date(2025, 8, 30)
        end_date = date(2025, 9, 10)
        LeaveRequestFactory.create(
            employee=test_employee,
            start_date=start_date,
            end_date=end_date,
            leave_type='casual',
            status='approved',
            approved_by=test_hr,
            approved_date=date(2025, 8, 28)
        )
        
        # Second leave request
        start_date = date(2025, 7, 27)
        end_date = date(2025, 8, 1)
        LeaveRequestFactory.create(
            employee=test_employee,
            start_date=start_date,
            end_date=end_date,
            leave_type='casual',
            status='approved',
            approved_by=test_hr,
            approved_date=date(2025, 7, 25)
        )
        
        # Third leave request
        start_date = date(2025, 8, 10)
        end_date = date(2025, 8, 11)
        LeaveRequestFactory.create(
            employee=test_employee,
            start_date=start_date,
            end_date=end_date,
            leave_type='casual',
            status='approved',
            approved_by=test_hr,
            approved_date=date(2025, 8, 9)
        )
        
       

@pytest.fixture
def create_attendance_for_month(db, test_employee, leave_request_conftest):
    
        records = []
    
    
        year, month = 2025, 8
        days_in_august = 31 
        leave_days = [1,  10, 11,  31]
        absent_days = [4, 5]
        halfday_days = [6, 7]

        for day in range(1, days_in_august + 1): 
            current_date = datetime.date(year, month, day)

            if current_date.weekday() == 5: 
                continue 
                
            if LeaveRequestService.check_leave_approval(test_employee.id, current_date): 
                status = 'leave'
                check_in = None 
                check_out = None 
                
            elif day in absent_days:
                status = 'absent'
                check_in = None
                check_out = None
            elif day in halfday_days:  
                status = "half-day"
                check_in = timezone.make_aware(datetime.datetime(year, month, day, 10, 0))
                check_out = timezone.make_aware(datetime.datetime(year, month, day, 14, 0))   
            else: 
                status = "present"
                check_in = timezone.make_aware(datetime.datetime(year, month, day, 9, 30))
                check_out = timezone.make_aware(datetime.datetime(year, month, day, 18, 0))

            record = AttendanceFactory(
                employee=test_employee,
                date=current_date,
                status=status,
                check_in=check_in,
                check_out=check_out
            )
            records.append(record)
        
     
    
        return records

@pytest.fixture
def attendance_with_overtime(create_attendance_for_month, test_employee, test_hr):
    
        valid_records = [r for r in create_attendance_for_month if r.status in ['present', 'half-day']]
        
        for record in valid_records[:5]: 
            overtime = OvertimeFactory.create(
                employee=test_employee,
                attendance=record,
                status='approved',
                approval_date=timezone.now(),
                approved_by=test_hr,
                requested_hour=2
            )
        
      

@pytest.fixture
def overtime_rate_conftest(db, test_employee):
   
        overtime = OvertimeRateFactory.create(employee=test_employee, overtime_rate=10)


@pytest.fixture
def allowance_creation(db,test_employee): 
      AllowanceFactory.create(employee=test_employee,amount=10000,allowance_type=AllowanceChoices.ALLOWANCE,month=date(2025,8,12))
      AllowanceFactory.create(employee=test_employee,amount=5000,allowance_type=AllowanceChoices.BONUS,month=date(2025,8,17))
      AllowanceFactory.create(employee=test_employee,amount=1000,allowance_type=AllowanceChoices.COMMISSION,month=date(2025,8,26))
      AllowanceFactory.create(employee=test_employee,amount=6000,allowance_type=AllowanceChoices.FESTIVAL_ALLOWANCE,month=date(2025,8,1))
      AllowanceFactory.create(employee=test_employee,amount=3000,allowance_type=AllowanceChoices.MEALS_ALLOWANCE,month=date(2025,8,14))


@pytest.fixture 
def deduction_creation(db,test_employee): 
      DeductionFactory.create(employee=test_employee,amount=1000,type=DeductionChoices.LATE_FINE,month=date(2025,8,10))      
      DeductionFactory.create(employee=test_employee,amount=1000,type=DeductionChoices.LATE_FINE,month=date(2025,8,11))      

@pytest.fixture
def tax_creation(db): 
           TaxFactory.create(starting_salary=0,ending_salary=600000,tax_percentage=1,taxpayer_type=TaxType.MARRIED)
           TaxFactory.create(starting_salary=600001,ending_salary=800000,tax_percentage=10,taxpayer_type=TaxType.MARRIED)
           TaxFactory.create(starting_salary=800001,ending_salary=1100000,tax_percentage=20,taxpayer_type=TaxType.MARRIED)
           TaxFactory.create(starting_salary=1100001,ending_salary=2000000,tax_percentage=30,taxpayer_type=TaxType.MARRIED)
           TaxFactory.create(starting_salary=2000001,ending_salary=5000000,tax_percentage=36,taxpayer_type=TaxType.MARRIED)
           TaxFactory.create(starting_salary=5000001,ending_salary=None,tax_percentage=36,taxpayer_type=TaxType.MARRIED)
