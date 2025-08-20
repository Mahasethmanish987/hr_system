from django.db import models 
from employee_module.models import TimeStamp,Employee


class Attendance(TimeStamp): 
    STATUS_CHOICES=[
        ('present','Present'),
        ('absent','Absent'),
        ('half-day','Half-Day'),
        ('leave','leave'),
        ('in-progress','In-Progress'),
    ]

    employee=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name='attendace')
    date=models.DateField()
    check_in=models.TimeField(null=True,blank=True)
    check_out=models.TimeField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='in-progress')
    late_arrival=models.BooleanField(default=False)
    early_exit=models.BooleanField(default=False)

    class Meta: 
        unique_together=('employee','date')

    def __str__(self): 
           return f"{self.employee.employee_name}-{self.date}" 

class WorkingSummary(TimeStamp): 
     
     attendance=models.OneToOneField(Attendance,on_delete=models.SET_NULL,null=True,blank=True)
     worked_hours=models.FloatField(default=0)
     overtime_hours=models.FloatField(default=0)
     total_hours=models.FloatField(default=0)


     def __str__(self): 
          return f"summary: {self.attendance}"
     

class OvertimeRequest(TimeStamp): 
     STATUS_CHOICES=[
          ('pending',"Pending"),
            ('approved',"Approved"),
          ('rejected',"Rejected"),
     ]
     employee=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name='overtime_request')
     attendance=models.ForeignKey(Attendance,on_delete=models.SET_NULL,null=True,blank=True)
     requested_hour=models.FloatField()
     status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
     request_date= models.DateTimeField(auto_now_add=True)
     approval_date=models.DateTimeField(null=True,blank=True)
     approved_by=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)
     