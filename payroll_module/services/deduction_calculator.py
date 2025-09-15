from employee_module.models import Employee
from datetime import date 
from abc import ABC,abstractmethod
from decimal import Decimal 
from payroll_module.models import Deduction 
from django.db.models import Sum


class DeductionService: 

      @staticmethod
      def get_deductions(employee:Employee,starting_date,ending_date)->dict: 
            return {
                  "normal_deduction":NormalDeduction.calculate(employee,starting_date,ending_date)
            }

class DeductionCalculator(ABC): 

    @abstractmethod
    def calculate(employee:Employee,starting_date:date,ending_date:date)->Decimal: 
           pass 


class NormalDeduction(DeductionCalculator): 
      @staticmethod
      def calculate(employee:Employee,starting_date:date,ending_date:date)->Decimal: 
            deduction_amount=Deduction.objects.filter(employee=employee,month__range=[starting_date,ending_date]).aggregate(total=Sum('amount'))['total'] or 0 

            return deduction_amount