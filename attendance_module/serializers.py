from django.utils import timezone
from employee_module.models import Employee
from rest_framework import serializers
from django.utils.dateformat import format
import datetime


from .models import Attendance, OvertimeRequest,WorkingSummary,AttendanceAuditLog


class PunchSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()

    def validate_employee_id(self, value):
        """Ensure the employee exists and is active"""

        try:
            employee = Employee.objects.get(id=value, is_active=True)

        except Employee.DoesNotExist:
            raise serializers.ValidationError("invalid or inactive employee id")

        return value


class OvertimeSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateField(write_only=True)

    class Meta:
        model = OvertimeRequest
        fields = [
            "id",
            "date",
            "requested_hour",
            "employee",
            "status",
            "approved_by",
            "request_date",
            "approval_date",
        ]
        read_only_fields = [
            "status",
            "request_date",
            "approved_by",
            "approval_date",
            "employee",
        ]

    def validate_date(self, value):
        """Ensure the date is not in the future"""
        if value > timezone.localdate():
            raise serializers.ValidationError("Date cannot be in the future")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        date = validated_data.pop("date")

        try:
            attendance = Attendance.objects.get(employee=user.employee, date=date)
        except Attendance.DoesNotExist:
            raise serializers.ValidationError(
                {"date": "No attendance found for this date."}
            )
        if not attendance.check_in:
            raise serializers.ValidationError(
                {"date": "Cannot request overtime for a day when not checked in."}
            )

        return OvertimeRequest.objects.create(
            employee=user.employee, attendance=attendance, **validated_data
        )

class OvertimeApproveSerializer(serializers.ModelSerializer):

    class Meta:
        model = OvertimeRequest
        fields = [
            "id",
            
            "status",
            "approved_by",
            "approval_date",
        ]
        read_only_fields = [
            "requested_hour",
            "approved_by",
            "approval_date",
        ]  

    def update(self, instance, validated_data):
            user = self.context["request"].user
            if instance.status != "pending":
                raise serializers.ValidationError(
                    {"status": "Only pending requests can be updated."}
                )
            instance.status = validated_data.get("status", instance.status)
            
            if instance.employee == user.employee:
                raise serializers.ValidationError(
                    {"status": "You cannot approve/reject your own request."}
                )
            if instance.status in ["approved", "rejected"]:
                instance.approved_by = user.employee
                instance.approval_date = timezone.now()
            instance.save()
            return instance


class WorkingSummarySerializer(serializers.ModelSerializer): 
    class Meta: 
        model=WorkingSummary
        fields=[
            "id",
            "worked_hours",
            "overtime_hours",
            "total_hours"]
        

class AttendanceListSerializer(serializers.ModelSerializer):
    working_summary = WorkingSummarySerializer(read_only=True, source='workingsummary')
    check_in_local = serializers.SerializerMethodField()
    check_out_local = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields=[
            "id",
            "check_in",
            "check_out",
            "check_in_local",
            "check_out_local",
            "status",
            "late_arrival",
            "early_exit",  
            "working_summary"     
            
        ]
        read_only_fields = ["status","late_arrival","early_exit","working_summary"]
    
    def get_check_in_local(self, obj):
        if obj.check_in:
            return timezone.localtime(obj.check_in).strftime("%Y-%m-%d %H:%M:%S")
        return None

    def get_check_out_local(self, obj):
        if obj.check_out:
            return timezone.localtime(obj.check_out).strftime("%Y-%m-%d %H:%M:%S")
        return None
    def update(self, instance, validated_data):
      changes = {}

      for attr, new_value in validated_data.items():
        old_value = getattr(instance, attr)
        if old_value != new_value:
            
             old_val_for_log = old_value.isoformat() if isinstance(old_value, (datetime.datetime, datetime.date)) else old_value
             new_val_for_log = new_value.isoformat() if isinstance(new_value, (datetime.datetime, datetime.date)) else new_value
  
             changes[attr] = {"old": old_val_for_log, "new": new_val_for_log}
             setattr(instance, attr, new_value)

      instance.save()

      if changes:
        AttendanceAuditLog.objects.create(
            attendance=instance,
            changed_by=self.context["request"].user.employee,
            changes=changes
        )

      return instance
    
        
            