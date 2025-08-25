from django.db import models
from employee_module.models import TimeStamp,Employee
# Create your models here.

class LeaveBalance(TimeStamp): 

    employee=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name="leave_balances") 
    month=models.DateField(help_text="Month and Year for which the balance is calculated")
    casual_leave=models.IntegerField(default=0)
    sick_leave=models.IntegerField(default=0)   
    

    class Meta: 
        unique_together = ('employee','month')
        ordering = ['-month']
    
   

    def __str__(self): 
        return f"{self.employee} - {self.month.strftime('%B %Y')}"    
    

class LeaveRequest(TimeStamp): 
    
    LEAVE_TYPE_CHOICES=[ 
        ("casual","Casual Leave"), 
        ("sick","Sick Leave"), 
    ]
    

