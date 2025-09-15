from django.contrib import admin
from .models import LeaveBalance, LeaveRequest

# Register LeaveBalance
@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'casual_leaves', 'sick_leaves')
    list_filter = ('month', 'employee')
    search_fields = ('employee__user__username',)

# Register LeaveRequest
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'days', 'status', 'approved_by', 'approved_date')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    search_fields = ('employee__user__username', 'reason')
    readonly_fields = ('days',)
