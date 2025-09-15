from django.db import models
from employee_module.models import Employee, TimeStamp

# Create your models here.


class AllowanceChoices(models.TextChoices):
    ALLOWANCE = "allowance", "Allowance"
    BONUS = "bonus", "Bonus"
    COMMISSION = "commission", "Commission"
    FESTIVAL_ALLOWANCE="festival_allowance","festival allowance"
    MEALS_ALLOWANCE='meals_allowance','meals_allowance'


class DeductionChoices(models.TextChoices):
    LATE_FINE = "late_fine", "Late Fine / Penalty"


class Allowance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="allowances",
    )
    month = models.DateField()
    allowance_type = models.CharField(max_length=20, choices=AllowanceChoices.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_taxable = models.BooleanField(default=False)
    is_annual=models.BooleanField(default=False)

    def save(self,*args,**kwargs): 
        TAXABLE_TYPES=   {"allowance","bonus","commission",'festival_allowance'}
        if self.allowance_type in TAXABLE_TYPES: 
            self.is_taxable=True 
        else: 
            self.is_taxable=False 


        ANNUAL_TYPES={"allowance"}

        if self.allowance_type in ANNUAL_TYPES: 
            self.is_annual=True
        else: 
            self.is_annual =False     

        super().save(*args,**kwargs)     


class Deduction(TimeStamp):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deduction",
    )
    month = models.DateField()
    type = models.CharField(max_length=20, choices=DeductionChoices.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class TaxType(models.TextChoices): 
    SINGLE= "unmarried","Unmarried"
    MARRIED='married','Married'

class Tax(TimeStamp):
  
    tax_name = models.CharField(max_length=255)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    starting_salary = models.DecimalField(max_digits=10, decimal_places=2)
    ending_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    taxpayer_type=models.CharField(max_length=20,choices=TaxType.choices)

    class Meta:
        unique_together = (
            "taxpayer_type",
            "tax_name",
            "starting_salary",
            "ending_salary",
        )

    def __str__(self):
        return f"{self.tax_name}---{self.tax_percentage}%"


class Salary(TimeStamp):
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,related_name='salary'
    )
    year = models.PositiveSmallIntegerField()
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_pay=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    allowances_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deduction_amount=models.DecimalField(max_digits=10,decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paying_structure = models.JSONField()
    salary_pdf = models.FileField(
        upload_to="media/salary/pdf_salary/", null=True, blank=True
    )

    class Meta:
        unique_together = ("year", "month", "employee")

    def __str__(self):
        return self.employee


class SalaryAuditTrail(TimeStamp):
    leave_balance = models.ForeignKey(
        Salary,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="salary_audit",
    )
    changed_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    changes = models.JSONField()

    def __str__(self):
        return f"Audit for {self.leave_balance} at {self.created_at}"


