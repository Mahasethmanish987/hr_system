from rest_framework import serializers

from .models import Attendance,OvertimeRequest,WorkingSummary
from employee_module.models import Employee


class AttendanceSerializer(serializers.Modelserializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = Attendance
        fields = [
            "employee",
            
            "check_in",
            "check_out",
            "status",
            "late_arrival",
            "early_exit",
        ]

class WorkingSummarySerializer(serializers.ModelSerializer): 
    employee = serializers.PrimaryKeyRelatedField(queryset=Attendance.objects.all())
    class Meta: 
        model=WorkingSummary
        fields=["attendance","worked_hour","overtime_hours","total_hours"]

class OvertimeSerializer(serializers.ModelSerializer): 
    pass 

