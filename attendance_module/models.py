from django.db import models
from employee_module.models import Employee, TimeStamp
from .utils import check_out_rules,apply_check_in,determine_status

class Attendance(TimeStamp):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("half-day", "Half-Day"),
        ("leave", "leave"),
        ("in-progress", "In-Progress"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendace",
    )
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in-progress"
    )
    late_arrival = models.BooleanField(default=False)
    early_exit = models.BooleanField(default=False)

    class Meta:
        unique_together = ("employee", "date")

    def __str__(self):
        return f"{self.employee.user.username}-{self.date}"

    def save(self, *args, **kwargs):
        if self.check_in:
            apply_check_in(self)

        if self.check_out:
            check_out_rules(self)
            determine_status(self)
        super().save(*args, **kwargs)


class WorkingSummary(TimeStamp):
    attendance = models.OneToOneField(
        Attendance, on_delete=models.SET_NULL, null=True, blank=True,related_name='working_summary'
    )
    worked_hours = models.FloatField(default=0)
    overtime_hours = models.FloatField(default=0)
    total_hours = models.FloatField(default=0)

    def __str__(self):
        return f"summary: {self.attendance}"
    
    


class OvertimeRequest(TimeStamp):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="overtime_request",
    )
    attendance = models.OneToOneField(
        Attendance, on_delete=models.SET_NULL, null=True, blank=True,related_name='overtime_request'
    )
    requested_hour = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta: 

        unique_together = ('employee', 'attendance')


class AttendanceAuditLog(TimeStamp): 
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )
    changed_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    changes = models.JSONField()
    def __str__(self):
        return f"Attendance {self.attendance.id} changed by {self.changed_by} at {self.changed_at}"


class OvertimeRate(TimeStamp):

    employee=models.OneToOneField(Employee,on_delete=models.SET_NULL,null=True,blank=True,related_name='overtime_rate')
    overtime_rate=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self): 
            return f"{self.employee.user.username} - {self.overtime_rate} per hour"
