import calendar
from datetime import date
from decimal import Decimal

from attendance_module.services.attendance_services import AttendanceService
from employee_module.models import Employee
from employee_module.services.employeedata_services import EmployeeDataService
from leave_module.services.leave_services import LeaveQuotaService, LeaveRequestService

from payroll_module.models import Allowance, Deduction
from payroll_module.services.allowance_calculator import AllowanceService
from payroll_module.services.deduction_calculator import DeductionService
from payroll_module.services.payroll_services import PayrollWriteService
from payroll_module.services.tax_calculator import TaxService


def count_working_days(target_month: date) -> int:
    year, month = target_month.year, target_month.month

    _, days_in_month = calendar.monthrange(year, month)

    working_days = 0

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        if d.weekday() == 5:
            continue
        working_days += 1
    return working_days


def get_total_allowance_by_month(employee_id: id, target_month: date) -> dict:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)

    allowances = Allowance.objects.filter(
        employee__id=employee_id, month__range=[start_date, end_date]
    )
    result = {"taxable": {"monthly": [], "annualizable": []}, "non_taxable": []}

    for allowance in allowances:
        allowance_detail = {
            "type": allowance.allowance_type,
            "amount": float(allowance.amount),
            "month": allowance.month.isoformat(),
            "is_annual": allowance.is_annual,
        }

        if allowance.is_taxable:
            if allowance.is_annual:
                result["taxable"]["annualizable"].append(allowance_detail)
            else:
                result["taxable"]["monthly"].append(allowance_detail)
        else:
            result["non_taxable"].append(allowance_detail)

    return result

def get_total_deductions_by_month(employee_id, target_month: date) -> dict:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)

    deductions = Deduction.objects.filter(
        employee__id=employee_id, month__range=[start_date, end_date]
    )

    total_amount = Decimal(0)
    details = []

    for deduction in deductions:
        deduction_detail = {
            "type": deduction.type,
            "amount": float(deduction.amount),  
            "month": deduction.month.isoformat(),
        }
        details.append(deduction_detail)
        total_amount += deduction.amount

    return {
        "total_amount": float(total_amount),
        "details": details,
    }


def create_payroll(
    employee_id: int,
    target_month: date,
    basic_salary: Decimal,
    overtime_pay: Decimal,
    total_allowance_pay: Decimal,
    total_deduction_amount: Decimal,
    tax: Decimal,
    net_salary: Decimal,
):
    salary_year = target_month.year
    salary_month = date(target_month.year, target_month.month, 1)
    deduction_dict = get_total_deductions_by_month(employee_id, target_month)
    allowance_dict = get_total_allowance_by_month(employee_id, target_month)
    PayrollWriteService.create_salary(
        employee_id,
        salary_year,
        salary_month,
        basic_salary,
        overtime_pay,
        tax,
        total_allowance_pay,
        total_deduction_amount,
        allowance_dict,
        deduction_dict,
        net_salary
    )


def calculate_net_salary(employee_id: int, target_month: date) -> float:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)

    total_working_days = count_working_days(target_month)

    attendance_details = AttendanceService.get_attendance_datail_by_month(
        employee_id, start_date, end_date
    )
    employee_salary_detail = EmployeeDataService.get_employee_payment_detail(
        employee_id
    )
    current_salary = employee_salary_detail.get("salary")
   
    overtime_hour_rate = employee_salary_detail.get("overtime_hour_rate")
    marital_status = employee_salary_detail.get("marital_status")
    base_salary, overtime_pay = calculate_basic_salary(
        employee_id,
        current_salary,
        overtime_hour_rate,
        attendance_details,
        total_working_days,
        target_month,
    )

    annualized_allowance, one_time_allowance, non_taxable_allowances = (
        calculate_allowance(employee_id, start_date, end_date)
    )
    deduction = calculate_deduction(employee_id, start_date, end_date)
    tax = calculate_tax(
        marital_status, base_salary, annualized_allowance, one_time_allowance, deduction
    )

    net_salary = (
        base_salary
        + annualized_allowance
        + one_time_allowance
        + non_taxable_allowances
        - deduction
        - tax
    )
    total_allowance = annualized_allowance + one_time_allowance + non_taxable_allowances
    create_payroll(
        employee_id,target_month,base_salary,overtime_pay,  total_allowance, deduction, tax, net_salary
    )
    

def calculate_allowance(
    employee_id: Employee, starting_date: date, ending_date: date
) -> tuple | None:
    allowances = AllowanceService.get_allowances(
        employee_id, starting_date, ending_date
    )
    taxable_allowances = allowances["taxable_allowance"]
    non_taxable_allowances = allowances["non_taxable_allowance"]

    return (
        taxable_allowances["annualized_allowance"],
        taxable_allowances["one_time_allowance"],
        non_taxable_allowances,
    )


def calculate_deduction(
    employee_id: int, starting_date, ending_date: date
) -> Decimal | None:
    deductions = DeductionService.get_deductions(
        employee_id, starting_date, ending_date
    )
    total_amount = 0
    for key, value in deductions.items():
        total_amount += value
    return total_amount


def calculate_tax(
    marital_status, base_salary, annualized_allowance, one_time_allowance, deductions
) -> Decimal | None:
    total_taxable_amount = (
        Decimal(base_salary) * 12 + Decimal(annualized_allowance) * 12 + one_time_allowance - deductions
    )
    total_taxable_amount = Decimal(str(total_taxable_amount))
    tax = TaxService.calculate(marital_status, total_taxable_amount)
    return tax


def determine_used_unused_leave(leave_balance: int, approved_leave: int) -> tuple:
    if leave_balance >= approved_leave:
        used_leave = approved_leave
        unused_leave = leave_balance - approved_leave
    else:
        unused_leave = 0
        used_leave = leave_balance

    return (used_leave, unused_leave)


def calculate_overtime_pay(overtime_rate: int, overtime_hours: Decimal):
    return overtime_rate * overtime_hours


def calculate_basic_salary(
    employee_id: int,
    basic_salary: int,
    overtime_hour_rate: int,
    attendance_records: dict,
    total_working_days: int,
    target_month: date,
) -> float:
    present_days = 0
    present_day = Decimal(attendance_records.get("present_day", 0))
    half_days = Decimal(attendance_records.get("half_day", 0)) * Decimal('0.5')
    overtime_hours = Decimal(attendance_records.get("overtime_hours", 0))

    present_days = present_day + half_days
    leave_quota = get_leave_quota(employee_id, target_month)

    approved_leave_balance = get_no_of_leave_approval(employee_id, target_month)

    used_leave, unused_leave = determine_used_unused_leave(
        leave_quota,  approved_leave_balance
    )

    total_days = present_days + used_leave
    if total_days >= total_working_days:
        total_days = total_working_days
    else:
        pass

    payable_salary = (basic_salary / Decimal(total_working_days)) * total_days

    update_leave_balance(employee_id,target_month, unused_leave)
    overtime_pay = calculate_overtime_pay(overtime_hour_rate, overtime_hours)

    return round(payable_salary + overtime_pay, 2), overtime_pay


def get_no_of_leave_approval(employee_id: int, target_month: date) -> int:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)

    approved_leave_days = LeaveRequestService.get_approved_leave(
        employee_id, start_date, end_date
    )

    return approved_leave_days


def get_leave_quota(employee_id: int, target_month) -> int:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    leave_balance = LeaveQuotaService.get_leave_quota(employee_id, start_date)

    if leave_balance:
        return leave_balance["sick_leaves"] + leave_balance["casual_leaves"]
    return 0


def update_leave_balance(
    employee_id: int, target_month: date, unused_leaves: int
) -> None:
    year, month = target_month.year, target_month.month
    start_date = date(year, month, 1)
    leave_data = {"casual_leaves": unused_leaves, "sick_leaves": 0}
    leave_quota = LeaveQuotaService.update_leave_quota(
        employee_id, start_date, leave_data
    )
