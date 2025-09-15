from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance,OvertimeRequest,WorkingSummary
from .utils import calculate_working_summary



@receiver(post_save,sender=Attendance)
def create_summary(sender,instance,created,**kwargs): 
    if created: 
        return 
        
    if instance.status == "absent":
        WorkingSummary.objects.get_or_create(
            attendance=instance,)

    if instance.check_in and instance.check_out: 

        calculate_working_summary(instance)



@receiver(post_save,sender=OvertimeRequest)
def update_work_summary(sender,instance,created,**kwargs): 

    if instance.status != "approved":
        return
    attendance = instance.attendance
    if not attendance:
        return
    summary, created = WorkingSummary.objects.get_or_create(attendance=attendance)
    summary.overtime_hours += instance.requested_hour
    summary.total_hours = summary.worked_hours + summary.overtime_hours
    summary.save()
    