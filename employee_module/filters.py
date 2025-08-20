import django_filters
from .models import Employee
class EmployeeFilter(django_filters.FilterSet):
    employee_code = django_filters.CharFilter(
        field_name="employee_code", lookup_expr="exact"
    )
    department = django_filters.CharFilter(
        field_name="department__name", lookup_expr="icontains"
    )
    job_title = django_filters.CharFilter(
        field_name="job_title__job_title", lookup_expr="icontains"
    )
    username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )

    class Meta: 
        model=Employee 
        fields=["employee_code","department","job_title","username"]
