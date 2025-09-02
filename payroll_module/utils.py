import calendar
from datetime import date

from attendance_module.models import Attendance
from django.db.models import QuerySet
from employee_module.models import Employee
from leave_module.models import LeaveBalance, LeaveRequest
from leave_module.tasks import get_previous_month


def count_working_days(current_date: date) -> int:
    prev_month_date = get_previous_month(current_date)
    year, month = prev_month_date.year, prev_month_date.month

    _, days_in_month = calendar.monthrange(year, month)

    working_days = 0

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        if d.weekday() == 5:
            continue
        working_days += 1
    return working_days


def calculate_net_salary(employee: Employee) -> float:
    prev_month = get_previous_month(date.today())
    year, month = prev_month.year, prev_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)

    total_working_days = count_working_days(prev_month)

    attendance_records = Attendance.objects.filter(
        employee=employee, date__range=(start_date, end_date)
    ).select_related("working_summary")

    salary = calculate_basic_salary(employee, attendance_records, total_working_days)
    return salary 


def determine_used_unused_leave(leave_balance: int, approved_leave: int) -> tuple:
    if leave_balance >= approved_leave:
        used_leave = approved_leave
        unused_leave = leave_balance - approved_leave
    else:
        unused_leave = 0
        used_leave = leave_balance

    return (used_leave, unused_leave)


def calculate_overtime_pay(
    employee: Employee, attendance_records: QuerySet[Attendance]
):
    total_overtime = sum(
        attendance.working_summary.overtime_hours
        for attendance in attendance_records
        if hasattr(attendance, "working_summary") and attendance.working_summary
    )
    if employee.overtime_rate and employee.overtime_rate.overtime_rate : 
        overtime_rate=employee.overtime_rate.overtime_rate 
    else: 
        overtime_rate=0      

    return overtime_rate * total_overtime


def calculate_basic_salary(
    employee: Employee,
    attendance_records: QuerySet[Attendance],
    total_working_days: int,
) -> float:
    present_days = 0
    present_day = attendance_records.filter(status="present").count()
    half_days = attendance_records.filter(status="half-day").count() * 0.5

    present_days = present_day + half_days
    leave_quota = get_leave_quota(employee)
    approved_leave_balance = get_no_of_leave_approval(employee)

    used_leave, unused_leave = determine_used_unused_leave(
        leave_quota, approved_leave_balance
    )

    total_days = present_days + used_leave
    if total_days >= total_working_days:
        total_days = total_working_days
    else:
        pass

    basic_salary = employee.salary

    payable_salary = (basic_salary / total_working_days) * total_days

    update_leave_balance(employee, unused_leave)
    overtime_pay =calculate_overtime_pay(employee,attendance_records)


    return payable_salary +overtime_pay


def get_no_of_leave_approval(employee: Employee) -> int:
    prev_month = get_previous_month(date.today())
    year, month = prev_month.year, prev_month.month
    start_date = date(year, month, 1)
    _, last_date = calendar.monthrange(year, month)
    end_date = date(year, month, last_date)
    leave_requests = LeaveRequest.objects.filter(
        employee=employee,
        end_date__gte=start_date,
        start_date__lte=end_date,
        status="approved",
    )

    approved_leave_days = 0
    for leave_request in leave_requests:
        leave_start = max(leave_request.start_date, start_date)
        leave_end = min(leave_request.end_date, end_date)
        approved_leave_days += (leave_end - leave_start).days + 1

    return approved_leave_days


def get_leave_balance(employee: Employee, start_date: date) -> LeaveBalance:
    leave_balance = LeaveBalance.objects.filter(
        employee=employee, month=start_date
    ).first()
    if leave_balance:
        return leave_balance
    return None


def get_leave_quota(employee: Employee) -> int:
    prev_month = get_previous_month(date.today())
    year, month = prev_month.year, prev_month.month
    start_date = date(year, month, 1)
    leave_balance = get_leave_balance(employee, start_date)

    if leave_balance:
        return leave_balance.casual_leaves + leave_balance.sick_leaves
    return 0


def update_leave_balance(employee: Employee, unused_leaves: int) -> None:
    prev_month = get_previous_month(date.today())
    year, month = prev_month.year, prev_month.month
    start_date = date(year, month, 1)
    leave_balance = get_leave_balance(employee, start_date)

    if leave_balance:
        leave_balance.casual_leaves = unused_leaves
        leave_balance.sick_leaves = 0
        leave_balance.save()
