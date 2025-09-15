from datetime import date 
from celery import shared_task
from employee_module.models import Employee
from django.db import transaction 
from .models import LeaveBalance 
from django.utils import timezone
import logging 

logger = logging.getLogger(__name__)
def get_previous_month(current_date:date)->date:

    year=current_date.year
    month=current_date.month
    if month==1: 
        prev_month=12 
        prev_year=year-1 

    else: 
        prev_month=month-1 
        prev_year=year 

    return date(prev_year,prev_month,1)
    

@shared_task 
def carry_forward_leave_balances(): 
    today=timezone.now().date()
    current_month=today.replace(day=1)


    last_month=get_previous_month(current_month)

    employees=Employee.objects.filter(is_active=True)

    for emp in employees: 

        try:
            with transaction.atomic(): 

                last_leave_balance=LeaveBalance.objects.filter(employee=emp,month=last_month).first()
                if not last_leave_balance: 
                    continue 
                carry_casual_leave=last_leave_balance.casual_leaves+1 
                carry_sick_leave=last_leave_balance.sick_leaves+1 

                LeaveBalance.objects.create(
                    employee=emp,
                    month=current_month,
                    casual_leaves=carry_casual_leave,
                    sick_leaves= carry_sick_leave 
                ) 
        except Exception as e: 
           logger.info('carry forward leave exception')

