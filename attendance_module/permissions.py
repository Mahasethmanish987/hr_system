from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated,BasePermission  
from rest_framework import permissions
from employee_module.models import Employee
from employee_module.permissions import check_hr,check_manager,check_normal_employee,check_superuser



class AttendancePermission(BasePermission): 
    def has_permission(self,request,view): 
        if not request.user.is_authenticated: 
             
             return False 
        
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        
        if request.method in ['PUT','PATCH']:
            return request.user.is_superuser or check_hr(request)
        return False
        

    