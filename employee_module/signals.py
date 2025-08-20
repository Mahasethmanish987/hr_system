
from .models import Department, JobTitle, Employee,EmergencyContact,EmployeeHistory,EmployeeProfile
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=Employee)
def create_employee_related(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(employee=instance)
        EmployeeHistory.objects.create(employee=instance)
        EmergencyContact.objects.create(employee=instance)