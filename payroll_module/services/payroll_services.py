from datetime import date
from payroll_module.models import Salary 
from decimal import Decimal 
from employee_module.models import Employee 


class PayrollWriteService:
    @staticmethod
    def create_salary(
        employee_id: int,
        salary_year: date,
        salary_month: date,
        basic_salary: Decimal,
        overtime_pay: Decimal,
        tax_amount: Decimal,
        total_allowance_amount:int,
        total_deduction_amount: int,
        allowance_dict:dict,
        deduction_dict:dict,
        net_salary:Decimal
    ) -> None:
        
        employee = Employee.objects.get(id=employee_id)

        # create salary object
        salary = Salary.objects.create(
            employee=employee,
            year=salary_year,
            month=salary_month,  
            basic_salary=basic_salary ,
            overtime_pay=overtime_pay,  
            tax_amount=tax_amount,
            allowances_amount=total_allowance_amount,
            deduction_amount=total_deduction_amount,
            net_amount=net_salary,
            paying_structure={
                "allowances": allowance_dict,
                "deductions": deduction_dict
            }
        )
        return salary
    
    @staticmethod
    def update_salary(salary_id:id,salary_data:dict)->None:
        
        salary=Salary.objects.get(id=salary_id)
        if not salary :
          pass 
        




class PayrollReadService: 

    def check_salary_exists_for_months(employee_id:id,target_month:date): 
        
        return Salary.objects.filter(employee__id=employee_id,month=target_month,year=target_month.year).exists()