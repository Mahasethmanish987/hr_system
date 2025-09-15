from leave_module.models import LeaveBalance,LeaveRequest
from datetime import date 
from employee_module.models import Employee
from datetime import timedelta 
class LeaveQuotaService: 
    
    
    @staticmethod
    def update_leave_quota(employee_id:int,month:date,leave_data:dict)->None: 
        leave_balance=LeaveBalance.objects.filter(employee__id=employee_id,month=month).first()

        
        for key,value in leave_data.items(): 
            
            setattr(leave_balance,key,value)
        leave_balance.save()    

    
        
    @staticmethod
    def get_leave_quota(employee_id:int,month:date)->dict: 
        
         leave_balance=LeaveBalance.objects.filter(employee__id=employee_id,month=month).first()
         return {
             'casual_leaves':leave_balance.casual_leaves,
             'sick_leaves':leave_balance.sick_leaves,
             'leave_balance_id':leave_balance.id
         }


class LeaveRequestService: 
    

    @staticmethod
    def get_approved_leave(employee_id:int,start_date:date,end_date:date)->int:
        leave_requests = LeaveRequest.objects.filter(
        employee__id=employee_id,
        end_date__gte=start_date,
        start_date__lte=end_date,
        status="approved",
    )
        approved_leave_days = 0
        for leave_request in leave_requests:
           leave_start = max(leave_request.start_date, start_date)
           leave_end = min(leave_request.end_date, end_date)
           approved_leave_days += LeaveRequestService.calculate_leave_days(leave_start,leave_end)

        return approved_leave_days

    @staticmethod
    def calculate_leave_days(start_date, end_date, holidays=None) -> int:
        holidays = holidays or set()
        days = 0
        current = start_date
        while current <= end_date:
            if current.weekday() not in (5,):
                days += 1
            current += timedelta(days=1)
        return days
    @staticmethod 
    def check_leave_approval(employee_id:id,date:date)->bool: 
        
        return LeaveRequest.objects.filter(
        employee__id=employee_id,
        start_date__lte=date,
        end_date__gte=date,
        status="approved"
    ).exists()
    