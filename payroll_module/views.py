from django.shortcuts import render
from .serializers import AllowanceSerializer,DeductionSerializer
# Create your views here.
from employee_module.permissions import check_hr,check_superuser,IsHrOrSuperUser
from rest_framework import viewsets
from .models import Allowance,Deduction
from .permissions import PayrollPermission
from .models import  Salary 

class AllowanceViewSet(viewsets.ModelViewSet): 

    queryset=Allowance.objects.all()
    serializer_class=AllowanceSerializer
    http_method_names=['get','post','put','patch']
    permission_classes=[PayrollPermission]
    def get_queryset(self): 
       user=self.request.user 
       if user.is_supseruser or check_hr(self.request):
           return Allowance.objects.all() 
       elif hasattr(user,'employee'): 
           return Allowance.objects.all()
           
    
class DeductionViewSet(viewsets.ModelViewSet): 

    queryset=Deduction.objects.all()
    serializer_class=DeductionSerializer
    http_method_names=['get','post','put','patch']

    def get_queryset(self): 
        user=self.request.user 
        if user.is_supseruser or check_hr(self.request):
           return Allowance.objects.all() 
        elif hasattr(user,'employee'): 
           return Allowance.objects.all()



class PaymentViewSet(viewsets.ModelViewSet): 
    queryest=Salary.objects.all()
    pass 