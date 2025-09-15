from django.db import models
from employee_module.models import Employee, TimeStamp


class LeaveBalance(TimeStamp):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_balances",
    )
    month = models.DateField()
    casual_leaves = models.PositiveIntegerField(default=0)
    sick_leaves = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("employee", "month")
        ordering = ["-month"]

    def __str__(self):
        return f"{self.employee} - {self.month.strftime('%B %Y')}"


class LeaveRequest(TimeStamp):
    LEAVE_TYPE_CHOICES = [
        ("casual", "Casual Leave"),
        ("sick", "Sick Leave"),
    ]

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
        related_name="leave_requests",
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leaves",
    )
    approved_date = models.DateField(null=True, blank=True)
    days = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        from leave_module.services.leave_services import LeaveRequestService

        if self.start_date and self.end_date:
            self.days = LeaveRequestService.calculate_leave_days(self.start_date,self.end_date)
        super().save(*args, **kwargs)


class LeaveBalanceAuditTrail(TimeStamp):
    leave_balance = models.ForeignKey(
        LeaveBalance,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_trails",
    )
    changed_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    changes = models.JSONField()

    def __str__(self):
        return f"Audit for {self.leave_balance} at {self.created_at}"


