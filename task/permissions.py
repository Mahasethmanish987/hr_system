from rest_framework.permissions import BasePermission 
from rest_framework import permissions 

from .models import Task ,SubTask
from employee_module.permissions import check_hr,check_manager,check_normal_employee,check_superuser

class TaskPermission(BasePermission):

    def has_permission(self,request,view): 
        if not request.user.is_authenticated: 
             
             return False 
        if request.method in permissions.SAFE_METHODS:
            return True 
        if request.method=='POST': 

            if check_superuser(request): 
                return True 
            if check_hr(request) or check_manager(request): 
                return True 
        return False 

    def has_object_permission(self,request,view,obj): 
        if not request.user.is_authenticated: 
             
             return False 

        if request.method in ["PUT","PATCH"]: 

            if check_normal_employee(request) and obj.assigned_to==request.user.employee: 
                return True 
            if check_manager(request) and obj.assigned_by==request.user.employee: 
                return True 
            if check_hr(request) or request.user.is_superuser: 
                return True 
            return False 

            
    

