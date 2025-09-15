from payroll_module.models import Salary 
from django.dispatch import receiver 
from django.db.models.signals import post_save
from .tasks import generate_pdf

@receiver(post_save,sender=Salary)
def get_generate_slip(sender,instance,created,**kwargs): 
    
    if created : 
       

       salary_data = {
          "salary_id":instance.id,
          'year':instance.year,
          'month':instance.month.strftime("%Y-%m-%d"),
          "salary_basic_salary": instance.basic_salary,
          "overtime_pay": instance.overtime_pay,
          "tax_amount": instance.tax_amount,
          "allowance_amount": instance.allowances_amount,
          "deduction_amount": instance.deduction_amount,
          "allowances": instance.paying_structure.get("allowances", {}),
          "deductions": instance.paying_structure.get("deductions", {}),
       }
       generate_pdf(salary_data)



