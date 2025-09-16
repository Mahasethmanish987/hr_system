from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from employee_module.services.employeedata_services import EmployeeWriteService
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


class EmployeeTypeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = EmployeeType
        fields = "__all__"


class EmployeeStatusSerialzier(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = EmployeeStatus
        fields = "__all__"


class EmployeeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "employee_code", "email"]
        read_only_fields = fields


class DepartmentSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    manager = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )

    manager_info = EmployeeNestedSerializer(source="manager", read_only=True)
    employees = EmployeeNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "department_code",
            "manager",
            "manager_info",
            "is_active",
            "employees",
        ]
        read_only_fields = ["department_code", "manager_info", "employees"]

    def create(self, validated_data: dict):
        manager = validated_data.pop("manager", None)

        department = Department.objects.create(**validated_data)

        if manager:
            department.manager = manager
            department.save()
        return department

    def update(self, instance, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)

        if "manager" in validated_data:
            instance.manager = validated_data.get("manager")
        instance.save()    
        return instance


class DepartmentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name"]


class JobTitleSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)

    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    department_info = DepartmentNestedSerializer(source="department", read_only=True)

    class Meta:
        model = JobTitle
        fields = ["id","job_title", "department", "is_active", "department_info"]
        read_only_fields = ["id"]


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ["username", "password", "email", "first_name", "last_name"]
        model = User

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    is_active = serializers.BooleanField(required=False, default=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    job_title = serializers.PrimaryKeyRelatedField(queryset=JobTitle.objects.all())
    employee_type = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeType.objects.all()
    )
    employee_status = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all()
    )
    reporting_manager = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    employee_code = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "phone_number",
            "is_active",
            "employee_code",
            "dob",
            "user",
            "department",
            "job_title",
            "employee_type",
            "employee_status",
            "reporting_manager",
            "current_address",
            "permanent_address",
            "gender",
            "email",
            "marital_status",
            "current_salary",
        ]
        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data: dict) -> Employee:
        user_data = validated_data.pop("user", None)
        user = User.objects.create_user(**user_data)  # create the User
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
    
    def update(self,instance,validated_data:dict)->Employee: 
          employee=EmployeeWriteService.update(instance.id,validated_data)
          return employee 


class EmergencyContactSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = EmergencyContact
        fields = ["employee", "name", "relationship", "contact_number"]


class EmployeeHistorySerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = EmployeeHistory
        fields = [
            "employee",
            "previous_company",
            "previous_salary",
            "previous_position",
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = EmployeeProfile
        fields = [
            "employee",
            "profile_photo",
            "citizenship",
            "pan_card",
            "contact_agreement",
        ]
