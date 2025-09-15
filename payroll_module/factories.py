import factory
from employee_module.factories import EmployeeFactory
from payroll_module.models import Allowance,Deduction,Tax,AllowanceChoices,DeductionChoices,TaxType
from datetime import date 


class AllowanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Allowance

    employee = factory.SubFactory(EmployeeFactory)
    month = None # fixed to August 1
    allowance_type = factory.Iterator([
        AllowanceChoices.ALLOWANCE,
        AllowanceChoices.BONUS,
        AllowanceChoices.COMMISSION,
        AllowanceChoices.FESTIVAL_ALLOWANCE,
        AllowanceChoices.MEALS_ALLOWANCE

    ])
    amount = 0
    is_taxable = False
    is_annual = False



class DeductionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Deduction

    employee = factory.SubFactory(EmployeeFactory)
    month = date(2025, 8, 1)  # fixed to August 1
    type = factory.Iterator([DeductionChoices.LATE_FINE])
    amount = 0

class TaxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tax

    tax_name = factory.Faker("word")
    tax_percentage = 0
    starting_salary = 0
    ending_salary = None 
    taxpayer_type = factory.Iterator([TaxType.SINGLE, TaxType.MARRIED])