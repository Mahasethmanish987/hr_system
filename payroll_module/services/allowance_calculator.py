from abc import ABC, abstractmethod
from decimal import Decimal

from datetime import date 
from django.db.models import Sum
from employee_module.models import Employee
from payroll_module.models import Allowance


class AllowanceCalcutor(ABC):
    @abstractmethod
    def calculate(employee: Employee, month: date) -> Decimal:
        pass


class TaxableAllowance(AllowanceCalcutor):
    pass 


class AnnualizedTaxable(TaxableAllowance):
    @staticmethod
    def calculate(employee: Employee, starting_date: date,ending_date:date) -> Decimal:
        
        allowance_amount = (
            Allowance.objects.filter(
                employee=employee,
                month__range=[starting_date,ending_date],
                is_taxable=True,
                is_annual=True,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return allowance_amount


class OneTimeTaxable(TaxableAllowance):
    @staticmethod
    def calculate(employee: Employee, starting_date:date,ending_date:date) -> Decimal:
        
        allowance_amount = (
            Allowance.objects.filter(
                employee=employee,
                month__range=[starting_date,ending_date],
                is_taxable=True,
                is_annual=False,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return allowance_amount



class NonTaxableAllowance(AllowanceCalcutor):
    @staticmethod
    def calculate(employee: Employee, starting_date: date,ending_date:date) -> Decimal:
        allowance_amount = (
            Allowance.objects.filter(
                employee=employee, month__range=[starting_date,ending_date], is_taxable=False
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return allowance_amount


class AllowanceService:

    @staticmethod 
    def get_allowances(employee:Employee,starting_date,ending_date)->None: 
        
        
        annualized_allowance=AnnualizedTaxable.calculate(employee,starting_date,ending_date)
        one_time_allowance=OneTimeTaxable.calculate(employee,starting_date,ending_date)
        non_taxable_allowance=NonTaxableAllowance.calculate(employee,starting_date,ending_date)
        return {
            "taxable_allowance":
            {
                "annualized_allowance":annualized_allowance,
                "one_time_allowance":one_time_allowance,

            },
            "non_taxable_allowance":non_taxable_allowance
            
            
            
        }
        