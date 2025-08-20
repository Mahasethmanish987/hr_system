from rest_framework import permissions
from rest_framework.permissions import BasePermission

from employee_module.models import Employee


def get_employee_role(user): 
    """helper to get employee role if exists ,else None """

    if not user.is_authenticated: 
        return None 
    try: 
        return user.employee.role 
    except Employee.DoesNotExist: 
        return None 
    
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


# class TaskPermission(BasePermission):
#     """Custom permission
#     - Only HR, Manager, Superuser can CREATE tasks.
#     - Any employee can UPDATE tasks assigned to them.
#     """

#     def has_permission(self, request, view):
#         user = request.user
#         if not user.is_authenticated:
#             return False

#         if request.method in permissions.SAFEMETHODS:
#             return True

#         if request.method == "POST":
#             if user.is_superuser:
#                 return True

#             if hasattr(user, "employee") and user.employee.role in [
#                 Employee.HR,
#                 Employee.MANAGER,
#                 Employee.OTHER,
#             ]:
#                 return False
#             return True
#         return True

#     def has_object_permission(self, request, view, obj):
#         if request.method in ["PUT", "PATCH"]:
#             if (
#                 hasattr(request.user, "employee")
#                 and obj.assigned_to == request.user.employee
#             ):
#                 return True
#             if (
#                 hasattr(request.user, "employee")
#                 and request.user.employee.role == Employee.MANAGER
#             ):
#                 if obj.assigned_by == request.user.employee:
#                     return True

#             if hasattr(request.user, "employee") and request.user.employee.role in [
#                 Employee.HR
#             ]:
#                 return True
#             if request.user.is_superuser:
#                 return True
#             return False
