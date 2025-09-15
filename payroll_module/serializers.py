from rest_framework  import serializers 
from .models import Allowance,Deduction
from employee_module.models import Employee
import datetime 
from django.utils import timezone 

class AllowanceSerializer(serializers.ModelSerializer): 
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta: 
        model=Allowance
        fields=['employee','type','amount']

    def create(self,validated_data): 
        month=timezone.localdate()
        allowance=Allowance.objects.create(**validated_data,month=month)
        return allowance

class DeductionSerializer(serializers.ModelSerializer): 
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta: 
        model=Deduction
        fields=['employee','type','amount']
    def create(self,validated_data): 

        month=timezone.localdate()
        deduction=Deduction.objects.create(**validated_data,month=month)
        return deduction
    