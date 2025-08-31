from django.utils import timezone
from employee_module.models import Employee
from employee_module.permissions import IsHrOrSuperUser
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import AttendancePermission

from .models import Attendance, OvertimeRequest
from .serializers import (
    AttendanceListSerializer,
    OvertimeApproveSerializer,
    OvertimeSerializer,
    PunchSerializer,
)


class PunchAPIView(APIView):
    def post(self, request):
        serializer = PunchSerializer(data=request.data)

        if serializer.is_valid():
            employee_id = serializer.validated_data["employee_id"]
            employee = Employee.objects.get(id=employee_id)
            today = timezone.localdate()
            attendance, created = Attendance.objects.get_or_create(
                employee=employee, date=today
            )

            now = timezone.now()

            if not attendance.check_in:
                attendance.check_in = now
            elif not attendance.check_out:
                attendance.check_out = now
            else:
                return Response(
                    {"message": "Already checked in and out for today"},
                    status=status.HTTP_200_OK,
                )
            attendance.save()
            return Response(
                {
                    "message": "Punch recorded successfully",
                    "check_in": timezone.localtime(attendance.check_in).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "check_out": timezone.localtime(attendance.check_out).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if attendance.check_out
                    else None,
                    "late_arrival": attendance.late_arrival,
                    "early_exit": attendance.early_exit,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeOvertimeViewSet(viewsets.ModelViewSet):
    serializer_class = OvertimeSerializer
    queryset = OvertimeRequest.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.employee.role == Employee.HR:
            return OvertimeRequest.objects.all()

        elif hasattr(user, "employee") and user.employee.role == Employee.MANAGER:
            return OvertimeRequest.objects.filter(
                employee__reporting_manager=user.employee
            ) | OvertimeRequest.objects.filter(employee__user=user)
        elif hasattr(user, "employee"):
            employee_queryset = OvertimeRequest.objects.filter(employee__user=user)
            print(employee_queryset)
            return employee_queryset
        else:
            return OvertimeRequest.objects.none()


class EmployeeOvertimeApproveViewSet(viewsets.ModelViewSet):
    serializer_class = OvertimeApproveSerializer
    queryset = OvertimeRequest.objects.all()
    permission_classes = [IsHrOrSuperUser]
    http_method_names = ["get", "patch"]



class AttendanceViewset(viewsets.ModelViewSet):
    serializer_class = AttendanceListSerializer
    queryset = Attendance.objects.all()
    permission_classes = [AttendancePermission]
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.employee.role == Employee.HR:
            return Attendance.objects.all()

        elif hasattr(user, "employee") and user.employee.role == Employee.MANAGER:
            return Attendance.objects.filter(
                employee__reporting_manager=user.employee
            ) | Attendance.objects.filter(employee__user=user)
        elif hasattr(user, "employee"):
            employee_queryset = Attendance.objects.filter(employee__user=user)
            print(employee_queryset)
            return employee_queryset
        else:
            return Attendance.objects.none()
