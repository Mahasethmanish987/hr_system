from django.utils import timezone
from employee_module.models import Employee
from employee_module.permissions import IsHrOrSuperUser
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import AttendancePermission,OvertimeRequestPermission

from .models import Attendance, OvertimeRequest
from .serializers import (
    AttendanceListSerializer,
    OvertimeApproveSerializer,
    OvertimeSerializer,
    PunchSerializer,
)
import logging 
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from rest_framework import exceptions
logger = logging.getLogger(__name__)
from django.db.models import Q 

class BaseAPIView(APIView):
    """Base view with DRY exception handling."""

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            logger.info(f"Resource not found (404): {str(exc)}")
            return Response(
                {"error": "The requested resource does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if isinstance(exc, ObjectDoesNotExist):
            logger.info(f"Resource not found: {str(exc)}")
            return Response(
                {"error": "Resource not found. Please check your request."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if isinstance(exc, IntegrityError):
            logger.warning(f"Data conflict detected: {str(exc)}")
            return Response(
                {"error": "Data conflicts with existing records."},
                status=status.HTTP_409_CONFLICT,
            )

        if isinstance(exc, DatabaseError):
            logger.error(f"Database failure: {str(exc)}", exc_info=True)
            return Response(
                {"error": "Database unavailable. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if isinstance(exc, exceptions.ValidationError):
            logger.warning(f"Validation error: {exc.detail}")
            return Response(
                {"validation_errors": exc.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Let DRF's default handler process unhandled exceptions
        logger.critical(f"Unexpected server error: {exc}", exc_info=True)
        return super().handle_exception(exc)


class PunchAPIView(BaseAPIView):
    def post(self, request):
        serializer = PunchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # handled by BaseAPIView if invalid

        employee_id = serializer.validated_data["employee_id"]
        employee = Employee.objects.get(id=employee_id)
        today = timezone.localdate()
        attendance, created = Attendance.objects.get_or_create(
            employee=employee, date=today
        )

        now = timezone.now()

        if not attendance.check_in:
            attendance.check_in = now
            message = "Checked in successfully"
        elif not attendance.check_out:
            attendance.check_out = now
            message = "Checked out successfully"
        else:
            return Response(
                {"message": "Already checked in and out for today"},
                status=status.HTTP_200_OK,
            )

        attendance.save()
        return Response(
            {
                "message": message,
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

class EmployeeOvertimeViewSet(viewsets.ModelViewSet):
    serializer_class = OvertimeSerializer
    queryset = OvertimeRequest.objects.all()
    permission_classes = [OvertimeRequestPermission]
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.employee.role == Employee.HR:
            return OvertimeRequest.objects.all()

        elif hasattr(user, "employee") and user.employee.role == Employee.MANAGER:
            return OvertimeRequest.objects.filter(
                Q(employee__reporting_manager=user.employee)| Q(employee__user=user)
            ) 
        elif hasattr(user, "employee"):
            employee_queryset = OvertimeRequest.objects.filter(employee__user=user)
           
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
                Q(employee__reporting_manager=user.employee)|Q(employee__user=user)
            ) 
        elif hasattr(user, "employee"):
            employee_queryset = Attendance.objects.filter(employee__user=user)
            
            return employee_queryset
        else:
            return Attendance.objects.none()
