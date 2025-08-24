from django.contrib import admin
from .models import Attendance, WorkingSummary, OvertimeRequest

# -----------------------------
# Attendance Admin
# -----------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "date",
        "check_in",
        "check_out",
        "status",
        "late_arrival",
        "early_exit",
    )
    list_filter = ("status", "late_arrival", "early_exit")
    search_fields = ("employee__user__username", "employee__user__username")
    date_hierarchy = "date"
    ordering = ("-date", "employee")


# -----------------------------
# WorkingSummary Admin
# -----------------------------
@admin.register(WorkingSummary)
class WorkingSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "attendance",
        "worked_hours",
        "overtime_hours",
        "total_hours",
    )
    search_fields = ("attendance__employee__user__username",)
    ordering = ("-attendance__date",)


# -----------------------------
# OvertimeRequest Admin
# -----------------------------
@admin.register(OvertimeRequest)
class OvertimeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "attendance",
        "requested_hour",
        "status",
        "request_date",
        "approval_date",
        "approved_by",
    )
    list_filter = ("status", "request_date")
    search_fields = ("employee__user__username",)
    ordering = ("-request_date",)
