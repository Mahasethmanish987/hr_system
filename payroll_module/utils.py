from attendance_module.models import Attendance 
from employee_module.models import Employee
from leave_module.tasks import  get_previous_month
import calendar 
from django.db.models import QuerySet
from datetime import date 
from leave_module.models import LeaveBalance

def count_working_days(current_date:date)->int:

  prev_month_date=get_previous_month(current_date)
  year,month=prev_month_date.year,prev_month_date.month 

  _,days_in_month= calendar.monthrange(year,month)

  working_days=0 

  for day in range(1,days_in_month+1): 
      d=date(year,month,day)
      if d.weekday() ==5: 
         continue 
      working_days+=1
  return working_days 

def calculate_net_salary(employee:Employee)->float:
    prev_month=get_previous_month(date.today())
    year,month=prev_month.year,prev_month.month
    start_date=date(year,month,1)
    _,last_date=calendar.monthrange(year,month)
    end_date=date(year,month,last_date)

    total_working_days=count_working_days(prev_month)

    
    

    attendance_records=Attendance.objects.filter(
       employee=employee,
       date__range=(start_date,end_date)
    )
     
    salary=calculate_basic_salary(employee,attendance_records,total_working_days)
    


def calculate_basic_salary(employee:Employee,attendance_records:QuerySet[Attendance],total_working_days:int)->float:


   present_days=0 
   for attendance_record in attendance_records: 
       if attendance_record.status =='present': 
          present_days+=1 
       elif attendance_record.status =='half-day':
          present_days+=0.5

   leave_quota=get_leave_quota(employee)

   total_days=present_days+leave_quota 
   if total_days>=total_working_days:
      unused_leave=total_days-total_working_days
      total_days=total_working_days
   else: 
      
      unused_leave=0 


   basic_salary=employee.salary    

   payable_salary=(basic_salary/total_working_days) * total_days

   update_leave_balance(employee,unused_leave)
   return payable_salary 

 




def get_leave_balance(employee:Employee,start_date:date)->LeaveBalance:
   leave_balance=LeaveBalance.objects.filter(employee=employee,month=start_date).first()
   if leave_balance:
      return leave_balance 
   return None 

def get_leave_quota(employee:Employee)->int: 

   prev_month=get_previous_month(date.today())
   year,month=prev_month.year,prev_month.month
   start_date=date(year,month,1)
   leave_balance=get_leave_balance(employee,start_date)

   if leave_balance: 
       return leave_balance.casual_leaves + leave_balance.sick_leaves
   return 0

def update_leave_balance(employee:Employee,unused_leaves:int)->None:
   prev_month=get_previous_month(date.today())
   year,month=prev_month.year,prev_month.month
   start_date=date(year,month,1)
   leave_balance=get_leave_balance(employee,start_date)

   if leave_balance:
      
      leave_balance.casual_leaves =  unused_leaves
      leave_balance.sick_leaves = 0 
      leave_balance.save()





          