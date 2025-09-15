from rest_framework import viewsets

from employee_module.permissions import IsHrOrSuperUser
from .filters import EmployeeFilter
from .models import (
    Department,
    EmergencyContact,
    Employee,
    EmployeeHistory,
    EmployeeProfile,
    EmployeeStatus,
    EmployeeType,
    JobTitle,
    
)
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    DepartmentSerializer,
    EmergencyContactSerializer,
    EmployeeHistorySerializer,
    EmployeeProfileSerializer,
    EmployeeSerializer,
    EmployeeStatusSerialzier,
    EmployeeTypeSerializer,
    JobTitleSerializer,
    
)
from django.db.models import Q 
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter
class EmployeeTypeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]

    


class EmployeeStatusViewSet(viewsets.ModelViewSet):
    queryset = EmployeeStatus.objects.all()
    serializer_class = EmployeeStatusSerialzier
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


class JobTitleViewSet(viewsets.ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "patch"]
    permission_classes=[IsAuthenticated]
    filter_backends=[DjangoFilterBackend]
    filterset_class=EmployeeFilter

    def get_queryset(self): 
        user=self.request.user 

        if user.is_superuser or user.employee.role==Employee.HR :
            employee_queryset= Employee.objects.all()
            
            return employee_queryset
        elif hasattr(user,'employee') and user.employee.role==Employee.MANAGER: 
            return Employee.objects.filter(Q(reporting_manager=user.employee)  |Q(user=user))
        elif hasattr(user,'employee'): 
            employee_queryset= Employee.objects.filter(user=user)
            
            return employee_queryset
        else: 
            return Employee.objects.none() 
         
    

    


class EmergencyContactViewset(viewsets.ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


class EmployeeHistoryViewSet(viewsets.ModelViewSet):
    queryset = EmployeeHistory.objects.all()
    serializer_class = EmployeeHistorySerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    lookup_field = "id"
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "post", "put", "patch"]


