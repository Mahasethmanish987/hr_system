from rest_framework import permissions
from rest_framework.permissions import BasePermission

from employee_module.models import Employee


def get_employee_role(user): 
    """helper to get employee role if exists ,else None """

    if not user.is_authenticated: 
        return False
    try: 
        return user.employee.role 
    except Employee.DoesNotExist: 
        return False 
    
def check_hr(request): 
    return get_employee_role(request.user)==Employee.HR    
def check_manager(request): 
    return get_employee_role(request.user)==Employee.MANAGER 
def check_normal_employee(request): 
    return get_employee_role(request.user)==Employee.OTHER 



def check_superuser(request): 
    return request.user.is_authenticated and request.user.is_superuser 


class IsHrOrSuperUser(BasePermission):
    """
    Custom permission to allow only HRs or Superusers.
    """

    def has_permission(self, request, view):
        
       if check_superuser(request): 
        return True 

        
       if check_hr(request): 
           return True 
       return False 


class IsAnonymousUser(BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated


class IsManagerOrSuperUserOrHr(BasePermission):
    def has_permission(self, request, view):
        
        if check_superuser(request): 
          return True 

        
        if check_hr(request): 
           return True 
        if check_manager(request): 
            return True 
    
        return False 


class  check_employee_viewset_permission(BasePermission):

    def has_permission(self,request,view): 
          if not  request.user.is_authenticated: 
              return False 
          if request.method in permissions.SAFE_METHODS:
            return True 
          
          if request.method in ["post",'patch',"get"]: 
              if check_hr(request) or request.user.is_superuser: 
                  return True 
          return False    