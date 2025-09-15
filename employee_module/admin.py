from django.contrib import admin
from .models import (
    Department, JobTitle, EmployeeType, EmployeeStatus, Employee,
    EmergencyContact, EmployeeProfile, EmployeeHistory,
    EmployeeTask, EmployeeTaskCompletion
)

# ------------------------
# INLINE ADMIN CLASSES
# ------------------------
class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    extra = 0

class EmployeeHistoryInline(admin.TabularInline):
    model = EmployeeHistory
    extra = 1


# ------------------------
# MAIN ADMIN CLASSES
# ------------------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department_code', 'manager', 'is_active', 'created_at')
    search_fields = ('name', 'department_code')
    list_filter = ('is_active',)
    ordering = ('name',)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'is_active')
    search_fields = ('job_title',)
    list_filter = ('department', 'is_active')


@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'user', 'job_title','email', 'department', 'employee_type', 'employee_status', 'reporting_manager', 'date_of_joining', 'is_active')
    search_fields = ('employee_code', 'role','email', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'employee_type', 'employee_status', 'is_active')
    ordering = ('employee_code',)
    inlines = [EmergencyContactInline, EmployeeProfileInline, EmployeeHistoryInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'employee_code', 'email', 'dob','phone_number' ,'gender')
        }),
        ('Address', {
            'fields': ('current_address', 'permanent_address')
        }),
        ('Work Details', {
            'fields': ('department','role','job_title', 'employee_type', 'employee_status', 'reporting_manager', 'date_of_joining','current_salary')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(EmployeeTask)
class EmployeeTaskAdmin(admin.ModelAdmin):
    list_display = ('employee_task_name', 'department', 'job_title', 'applies_to', 'employee_task_type', 'is_active')
    search_fields = ('employee_task_name',)
    list_filter = ('department', 'job_title', 'employee_task_type', 'is_active')


@admin.register(EmployeeTaskCompletion)
class EmployeeTaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('employee_task', 'performed_by_department', 'completed_task', 'created_at')
    list_filter = ('completed_task', 'performed_by_department')
    search_fields = ('employee_task__employee_task_name',)


# Inline for EmergencyContact
class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1  # number of empty forms shown

# Inline for EmployeeProfile
class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    extra = 0  # profile usually has only one record per employee

# Inline for EmployeeHistory
class EmployeeHistoryInline(admin.TabularInline):
    model = EmployeeHistory
    extra = 1




# If you also want them to be editable separately
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'name', 'relationship', 'contact_number')
    list_filter = ('relationship',)
    search_fields = ('name', 'employee__user__first_name', 'employee__user__last_name')


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'profile_photo', 'citizenship', 'pan_card', 'contact_agreement')


@admin.register(EmployeeHistory)
class EmployeeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'previous_company', 'previous_position', 'previous_salary')
    search_fields = ('previous_company', 'previous_position')
