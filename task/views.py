from employee_module.models import Employee
from rest_framework import viewsets

from task.models import SubTask, Task,OnboardingOffboardingTask
from employee_module.permissions import IsHrOrSuperUser
from .permissions import TaskPermission
from .serializers import SubTaskSerializer, TaskSerializer, OnboardingOffboardingTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "id"
    permission_classes = [TaskPermission]

    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.employee.role == Employee.HR:
            return Task.objects.all()
        elif hasattr(user, "employee") and user.employee.role == Employee.MANAGER:
            return Task.objects.filter(assigned_by=user.employee)
        elif hasattr(user, "employee"):
            return Task.objects.filter(assigned_to=user.employee)
        else:
            return Task.objects.none()


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = "id"
    permission_classes = [TaskPermission]

    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.employee.role == Employee.HR:
            return SubTask.objects.all()
        elif hasattr(user, "employee") and user.employee.role == Employee.MANAGER:
            return SubTask.objects.filter(assigned_by=user.employee)
        elif hasattr(user, "employee"):
            return SubTask.objects.filter(assigned_to=user.employee)
        else:
            return SubTask.objects.none()

class  OnboardingOffboardingTaskViewSet(viewsets.ModelViewSet): 

    queryset=OnboardingOffboardingTask.objects.all()
    serializer_class= OnboardingOffboardingTaskSerializer
    lookup_field='id'
    http_method_names = ["get", "post", "put", "patch"]
    permission_classes=[IsHrOrSuperUser]

