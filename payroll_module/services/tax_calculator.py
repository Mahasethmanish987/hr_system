from abc import ABC, abstractmethod
from decimal import Decimal
from employee_module.models import Employee
from payroll_module.models import Tax 
from django.db.models import QuerySet

class TaxService: 

    @staticmethod
    def calculate(marital_status:str,taxable_amount:Decimal)->Decimal: 
        
        if marital_status=='unmarried': 
            return unmarriedTaxCalculator.calculate_tax(taxable_amount)
        elif marital_status=='married': 
            return  MarriedTaxCalculator.calculate_tax(taxable_amount)


class TaxCalculator(ABC):
    @abstractmethod
    def calculate_tax(income: Decimal) -> Decimal:
        pass


class unmarriedTaxCalculator(TaxCalculator):
    @staticmethod
    def calculate_tax(
        income:Decimal
    ) -> Decimal:
        tax_slab=Tax.objects.filter(taxpayer_type='unmarried').order_by('starting_salary')

        tax_amount=calculate_tax_from_slabs(income,tax_slab)
        
        return round(tax_amount/12,2)

           


class MarriedTaxCalculator(TaxCalculator):
    @staticmethod
    def calculate_tax(
        income:Decimal
    ) -> Decimal:
        
        tax_slab=Tax.objects.filter(taxpayer_type='married').order_by('starting_salary')
        tax_amount=calculate_tax_from_slabs(income,tax_slab)
        
        return round(tax_amount/12,2)


def calculate_tax_from_slabs(income: Decimal, slabs: QuerySet[Tax]) -> Decimal:
    tax_due = Decimal('0')
    previous_max = Decimal('0')
    
    for slab in slabs:
        end = slab.ending_salary if slab.ending_salary is not None else income
        if income > previous_max:
            taxable_in_slab = min(income, end) - previous_max
            if taxable_in_slab > 0:
                slab_tax = taxable_in_slab * (Decimal(slab.tax_percentage) / Decimal('100'))
                tax_due += slab_tax
                previous_max = end
        else:
            break
    
    return tax_due.quantize(Decimal('0.01'))