from employee_module.models import Employee
from django.contrib.auth import get_user_model

class EmployeeDataService:
    @staticmethod
    def get_employee_payment_detail(employee_id: id) -> dict:
        employee = (
            Employee.objects.filter(id=employee_id)
            .prefetch_related("overtime_rate")
            .first()
        )
        if not employee:
            return
        return {
            "overtime_hour_rate": employee.overtime_rate.overtime_rate,
            "salary": employee.current_salary,
            "marital_status": employee.marital_status,
        }
    @staticmethod
    def get_all_employee_ids() -> list[int]:
        return list(
            Employee.objects.filter(is_active=True).values_list("id", flat=True)
        )
    
    @staticmethod 
    def get_employees_without_salary(target_month, target_year) -> list[int]:
        return list(
            Employee.objects.filter(is_active=True).exclude(
                salary__month=target_month, salary__year=target_year
            )
        .values_list("id", flat=True))
    

class EmployeeWriteService: 
    
    @staticmethod 
    def update(employe_id:id,validated_data:dict)->Employee:

        employee=Employee.objects.get(id=employe_id)
        if not employee: 
            pass 

        user=validated_data.pop('user',None)
        if user: 
            updated_user=UserWriteService.update(employee.user.id,user)
            employee.user=updated_user
        
        for key,value in validated_data.items(): 
            if hasattr(employee,key): 
                setattr(employee,key,value)

        employee.save()
        return employee 

User=get_user_model()
class UserWriteService: 

    @staticmethod 
    def update(user_id,validated_data:dict): 
       user=User.objects.get(id=user_id)
       if not user: 
           pass 
       for key,value in validated_data.items(): 
           if hasattr(user,key): 
               setattr(user,key,value)
       user.save()
       return user 
            
           
