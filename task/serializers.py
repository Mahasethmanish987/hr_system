from django.db import transaction
from employee_module.models import Department, Employee
from employee_module.serializers import EmployeeNestedSerializer
from rest_framework import serializers

from .models import SubTask, Task, OnboardingOffboardingTask


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True
    )
    assigned_to_details = EmployeeNestedSerializer(source="assigned_to", read_only=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            
            "title",
            "description",
            "priority",
            "due_date",
            "department",
            "assigned_to",
            "assigned_to_details",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not hasattr(request.user, "employee"):
            raise serializers.ValidationError(
                "Logged in user must have associated employee record"
            )

        assigned_by = request.user.employee

        with transaction.atomic():
            task = Task.objects.create(assigned_by=assigned_by, **validated_data)

        return task


class SubTaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True
    )
    assigned_to_details = EmployeeNestedSerializer(source="assigned_to", read_only=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )

    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "due_date",
            "department",
            "assigned_to",
            "assigned_to_details",
            "parent_task"
        ]
        read_only_fields=('id',)

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not hasattr(request.user, "employee"):
            raise serializers.ValidationError(
                "Logged in user must have associated employee record"
            )

        assigned_by = request.user.employee

        
        task = SubTask.objects.create(assigned_by=assigned_by, **validated_data)

        return task

class  OnboardingOffboardingTaskSerializer(serializers.ModelSerializer): 
      department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
      job_title = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )

      class Meta: 
          fields=["task_name","department","job_title","task_type","applies_to_all"]
          model= OnboardingOffboardingTask

      def create(self,validated_data): 
          
          request=self.context.get("request") 
          if not request or not hasattr(request.user, "employee"):
            raise serializers.ValidationError(
                "Logged in user must have associated employee record"
            )
          made_by=request.user.employee 
          task= OnboardingOffboardingTask.objects.create(made_by=made_by,**validated_data)
          return task 


                  