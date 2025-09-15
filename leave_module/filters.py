import django_filters

from .models import LeaveRequest


class LeaveRequestFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="start_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="end_date", lookup_expr="lte")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    username = django_filters.CharFilter(
        field_name="employee__user__username", lookup_expr="icontains"
    )

    department = django_filters.CharFilter(
        field_name="employee__department__name", lookup_expr="icontains"
    )

    date = django_filters.DateFilter(method="filter_by_date", label="Leave Date")
    

    class Meta:
        model = LeaveRequest
        fields = ["start_date", "end_date", "status", "username", "department", "date"]

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)
    


