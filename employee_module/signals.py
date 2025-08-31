
from .models import Department, JobTitle, Employee,EmergencyContact,EmployeeHistory,EmployeeProfile
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from leave_module.models import LeaveBalance 


@receiver(post_save,sender=Employee)
def create_employee_related(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(employee=instance)
        EmployeeHistory.objects.create(employee=instance)
        EmergencyContact.objects.create(employee=instance)



@receiver(post_save,sender=Employee)
def save_employee_leave_status(sender,instance,created,**kwargs):
        
        if created: 
             month = instance.date_of_joining.replace(day=1)

             
             LeaveBalance.objects.create(employee=instance,month=month,casual_leaves=1,sick_leaves=1)


      

