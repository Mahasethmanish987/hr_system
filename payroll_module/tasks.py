import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
from payroll_module.models import Salary
from celery import shared_task
from datetime import date 
from leave_module.tasks import get_previous_month 
from payroll_module.utils import calculate_net_salary
from employee_module.services.employeedata_services import EmployeeDataService
from payroll_module.services.payroll_services import PayrollReadService
import logging 
from django.db import transaction

logger = logging.getLogger(__name__)




@shared_task(name='calculate_salary')
def calculate_salary():
    current_month=date.today()
    target_month=get_previous_month(current_month)
    employe_ids=EmployeeDataService.get_employees_without_salary(target_month,target_month.year)
    for employee_id in employe_ids:
        
        
        try:
          with transaction.atomic(): 
             calculate_net_salary(employee_id,target_month)
        except Exception as e : 
            logger.error(f"problem of salary calculation of {employee_id} is {e}")



def generate_pdf(salary_data):
    salary = Salary.objects.get(id=salary_data["salary_id"])
    employee = salary.employee

    # PDF file path
    file_name = f"salary_{salary.id}_{salary.year}_{salary.month}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "salary/pdf_salary/", file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create PDF canvas
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Salary Slip")

    # Employee & totals
    c.setFont("Helvetica", 12)
    y_position = height - 100
    c.drawString(50, y_position, f"Employee: {employee}")
    y_position -= 20
    c.drawString(50, y_position, f"Basic Salary: {salary.basic_salary}")
    y_position -= 20
    c.drawString(50, y_position, f"Overtime Pay: {salary.overtime_pay}")
    y_position -= 20
    c.drawString(50, y_position, f"Tax Amount: {salary.tax_amount}")
    y_position -= 20
    c.drawString(50, y_position, f"Total Allowances: {salary.allowances_amount}")
    y_position -= 20
    c.drawString(50, y_position, f"Total Deductions: {salary.deduction_amount}")
    y_position -= 30

    # Allowances breakdown
    c.drawString(50, y_position, "Allowances Breakdown:")
    y_position -= 20
    allowances = salary.paying_structure.get("allowances", {})

    # Taxable
    taxable = allowances.get("taxable", {})
    for category, items in taxable.items():  # monthly / annualizable
        c.drawString(60, y_position, f"{category.capitalize()}:")
        y_position -= 15
        for item in items:
            c.drawString(70, y_position, f"{item['type']}: {item['amount']}")
            y_position -= 15

    # Non-taxable
    non_taxable = allowances.get("non_taxable", [])
    if non_taxable:
        c.drawString(60, y_position, "Non-taxable:")
        y_position -= 15
        for item in non_taxable:
            c.drawString(70, y_position, f"{item['type']}: {item['amount']}")
            y_position -= 15

    y_position -= 10

    # Deductions breakdown
    c.drawString(50, y_position, "Deductions Breakdown:")
    y_position -= 20
    deductions = salary.paying_structure.get("deductions", {}).get("details", [])
    for item in deductions:
        c.drawString(60, y_position, f"{item['type']}: {item['amount']}")
        y_position -= 15

    # Save PDF
    c.save()

    # Assign to model
    salary.salary_pdf.name = f"salary/pdf_salary/{file_name}"
    salary.save()

    print('Salary PDF saved at:', salary.salary_pdf)
