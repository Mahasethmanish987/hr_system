from datetime import date
from decimal import Decimal
from django.conf import settings 
import os 
import pytest
from PyPDF2 import PdfReader
from attendance_module.services.attendance_services import AttendanceService
from leave_module.services.leave_services import LeaveQuotaService

from payroll_module.models import Salary
from payroll_module.utils import (
    calculate_allowance,
    calculate_basic_salary,
    calculate_deduction,
    calculate_net_salary,
    calculate_overtime_pay,
    calculate_tax,
    count_working_days,
    determine_used_unused_leave,
    get_leave_quota,
    get_no_of_leave_approval,
    update_leave_balance,
)


def test_get_leave_quota(db, test_employee, leave_balance_conftest):
    target_month = date(2025, 8, 1)
    leave_quota = get_leave_quota(test_employee.id, target_month)
    assert leave_quota == 4


def test_update_leave_balance(db, test_employee, leave_balance_conftest):
    target_month = date(2025, 8, 1)
    unused_leave = 3
    update_leave_balance(test_employee.id, target_month, unused_leave)

    leave_quota_dict = LeaveQuotaService.get_leave_quota(test_employee.id, target_month)

    assert unused_leave == leave_quota_dict["casual_leaves"]
    assert 0 == leave_quota_dict["sick_leaves"]
    assert leave_quota_dict["leave_balance_id"] is not None


def test_count_approved_leave_of_months(db, test_employee, leave_request_conftest):
    target_month = date(2025, 8, 1)
    assert 4 == get_no_of_leave_approval(test_employee.id, target_month)


@pytest.mark.parametrize(
    "leave_balance, approved_leave, used_leave, unused_leave",
    [
        (5, 3, 3, 2),
        (3, 5, 3, 0),
    ],
)
def test_determine_leave_used_unused_leave(
    leave_balance, approved_leave, used_leave, unused_leave
):
    assert (used_leave, unused_leave) == determine_used_unused_leave(
        leave_balance, approved_leave
    )


@pytest.mark.parametrize(
    "target_month,expected_working_days",
    [
        (date(2025, 8, 1), 26),
        (date(2025, 9, 1), 26),
    ],
)
def test_calculate_total_working_days(target_month, expected_working_days):
    assert expected_working_days == count_working_days(target_month)


def test_calculate_basic_salary_checking_leave_balances(
    db,
    test_employee,
    leave_request_conftest,
    leave_balance_conftest,
    create_attendance_for_month,
    attendance_with_overtime,
    overtime_rate_conftest,
):
    start_date = date(2025, 8, 1)
    end_date = date(2025, 8, 31)
    attendance_records = AttendanceService.get_attendance_datail_by_month(
        test_employee.id, start_date, end_date
    )
    overtime_hours = attendance_records.get("overtime_hours")
    total_working_days = count_working_days(start_date)
    overtime_rate = test_employee.overtime_rate.overtime_rate
    basic_salary = calculate_basic_salary(
        test_employee.id,
        test_employee.current_salary,
        overtime_rate,
        attendance_records,
        total_working_days,
        start_date,
    )
    overtime_pay = calculate_overtime_pay(overtime_rate, overtime_hours)

    assert 100 == overtime_pay
    assert 88561.53, overtime_pay == basic_salary


def test_calculate_all_allowances(db, test_employee, allowance_creation):
    starting_date = date(2025, 8, 1)
    ending_date = date(2025, 8, 31)
    annualized_allowance = 10000
    monthly_allowance = 12000
    non_taxable_allowance = 3000
    assert (
        annualized_allowance,
        monthly_allowance,
        non_taxable_allowance,
    ) == calculate_allowance(test_employee.id, starting_date, ending_date)


def test_calculate_deduction(db, test_employee, deduction_creation):
    starting_date = date(2025, 8, 1)
    ending_date = date(2025, 8, 31)
    total_amount = 2000
    assert total_amount == calculate_deduction(
        test_employee.id, starting_date, ending_date
    )


def test_calculate_tax(db, test_employee, tax_creation):
    base_salary = 88561.53
    annualized_allowance = 10000
    one_time_allowance = 12000
    deduction = 2000
    marital_status = "married"
    expected_tax = Decimal("9485.13")
    tax = calculate_tax(
        marital_status, base_salary, annualized_allowance, one_time_allowance, deduction
    )

    assert tax == expected_tax


def test_calculate_net_salary(
    db,
    test_employee,
    allowance_creation,
    deduction_creation,
    tax_creation,
    create_attendance_for_month,
    overtime_rate_conftest,
    attendance_with_overtime,
    leave_balance_conftest,
    leave_request_conftest,
):
    target_month = date(2025, 8, 1)
    expected_net_salary = Decimal("102076.41")
    net_salary = calculate_net_salary(test_employee.id, target_month)

    salary = Salary.objects.get(employee__id=test_employee.id, month=target_month)
    print(
        "salary_basic_salary",
        salary.basic_salary,
        "overtime_pay:",
        salary.overtime_pay,
        "tax_amount",
        salary.tax_amount,
        "allowance_amount:",
        salary.allowances_amount,
        "deduction_amount:",
        salary.deduction_amount,
    )
    
    assert salary.net_amount == expected_net_salary
    salary.refresh_from_db()
    
    print(salary.salary_pdf,'these is the salary pdf ')
    pdf_path = salary.salary_pdf.path

    assert os.path.exists(pdf_path)

    
    reader = PdfReader(pdf_path)
    text_content = "".join(page.extract_text() for page in reader.pages)

    
    assert "Salary Slip" in text_content
    assert str(salary.basic_salary) in text_content
    assert str(salary.overtime_pay) in text_content
    assert str(salary.tax_amount) in text_content
    assert str(salary.allowances_amount) in text_content
    assert str(salary.deduction_amount) in text_content
    assert str(test_employee) in text_content