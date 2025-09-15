from rest_framework import serializers 
from .models import LeaveRequest,LeaveBalance,LeaveBalanceAuditTrail
from employee_module.models import Employee
from django.utils import timezone
from django.db import transaction 

class LeaveRequestSerializer(serializers.ModelSerializer):

    employee=serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()) 
    
    class Meta: 
        model=LeaveRequest
        fields=["employee","leave_type","start_date","end_date","reason","reason","status","approved_by","approved_date","days"]
        read_only_fields=["is_paid","days","approved_by","approved_date","status"]

    

class LeaveRequestStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta: 
        model=LeaveRequest 
        fields=["status"]
    
    def validate_status(self,value):
        if value not in ["approved","rejected"]:
            raise serializers.ValidationError("Status must be either 'approved' or 'rejected'.")
        return value
    
    def update(self,instance,validated_data):
        user_employee=self.context['request'].user.employee
        if instance.employee==user_employee:
            raise serializers.ValidationError("You cannot approve/reject your own leave request.")

        if instance.status in ["approved", "rejected"]:
            raise serializers.ValidationError("This leave request has already been processed.")
         
        instance.status=validated_data.get('status',instance.status)

        if instance.status in ["approved","rejected"]:

            instance.approved_by=self.context['request'].user.employee
            instance.approved_date= timezone.now().date()
        instance.save()
        return instance     
            


class LeaveBalanceUpdateSerializer(serializers.ModelSerializer): 
    
    class Meta: 
        model=LeaveBalance
        fields=['casual_leaves','sick_leaves']
        read_only_fields=['employee','month']

    @transaction.atomic
    def update(self,instance,validated_data): 
       
       user=self.context['request'].user

       old_data={
           'casual_leaves':instance.casual_leaves,
           'sick_leaves':instance.sick_leaves
       }
       instance.casual_leaves=validated_data.get('casual_leaves',instance.casual_leaves)
       instance.sick_leaves=validated_data.get('sick_leaves',instance.sick_leaves)
       instance.save()

       new_data={
           "casual_leaves":instance.casual_leaves,
           "sick_leaves":instance.sick_leaves   
       }

       changes={}
       for field in old_data:
            if old_data[field] != new_data[field]:
                changes[field] = {"old": old_data[field], "new": new_data[field]}
       if changes: 
           LeaveBalanceAuditTrail.objects.create(
               leave_balance=instance,
               changed_by=getattr(user,'employee',None),
               changes=changes 
           )

        
       return instance

