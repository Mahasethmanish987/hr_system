from rest_framework.permissions import BasePermission
from rest_framework import permissions 
from employee_module.permissions import check_hr,check_superuser

class PayrollPermission(BasePermission): 

    def has_permission(self, request, view):
        user=request.user 

        if not request.user.is_authenticated: 
            return False 
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        if request.method in ["post","put","patch"]: 
            return user.is_superuser or check_hr(request)
        return False 