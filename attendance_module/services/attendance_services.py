import logging
from datetime import date
from decimal import Decimal
from typing import Optional

from attendance_module.models import Attendance
from django.db.models import QuerySet, Sum,Q
from employee_module.models import Employee

logger = logging.getLogger(__name__)


class AttendanceService:
    @staticmethod
    def initialize_attendance_records_for_date(target_date: date):
        active_employees = Employee.objects.filter(is_active=True)
        created_count = 0
        existing_employee_ids = Attendance.objects.filter(date=target_date).values_list(
            "employee_id", flat=True
        )

        missing_employees = active_employees.exclude(id__in=existing_employee_ids)
        attendance_to_create = [
            Attendance(employee=emp, date=target_date) for emp in missing_employees
        ]
        Attendance.objects.bulk_create(attendance_to_create)
        logger.info(f"create attendance for {len(attendance_to_create)}")

    @staticmethod
    def update_attendance(attendance_id, data: dict) -> Attendance | None:
        attendance = Attendance.objects.filter(id=attendance_id).first()

        if not attendance:
            return None
        for key, value in data.items():
            setattr(attendance, key, value)

        attendance.save()
        return attendance

    @staticmethod
    def retrieve_attendance(
        employee_id: Optional[int] = None,
        date: Optional[date] = None,
        status: Optional[str] = None,
        
        check_in_isnull: Optional[bool] = None,
        check_out_isnull: Optional[bool] = None,
    ) -> QuerySet[Attendance] | None:
       
        filters=Q()

        if employee_id is not None: 
            filters&=Q(employee_id=employee_id)
        if date is not None: 
            filters&=Q(date=date)
        if status is not None:
            filters &= Q(status=status)
        if check_in_isnull is not None:
            filters &= Q(check_in__isnull=check_in_isnull)      
        if check_out_isnull is not None:
            filters &= Q(check_out__isnull=check_out_isnull)
        queryset = Attendance.objects.filter(filters).select_related("working_summary")    

        return queryset 

            

    @staticmethod
    def attendance_by_month(
        employee_id, start_date: date, end_date: date
    ) -> QuerySet[Attendance] | None:
        attendance_records = Attendance.objects.filter(
            employee__id=employee_id, date__range=[start_date, end_date]
        ).select_related("working_summary")
        return attendance_records

    @staticmethod
    def get_attendance_datail_by_month(employee_id, start_date:date, end_date: date) -> dict:
        attendance_records = AttendanceService.attendance_by_month(
            employee_id=employee_id, start_date=start_date, end_date=end_date
        )

        present_day = attendance_records.filter(status="present").count()
        half_day = attendance_records.filter(status="half-day").count()
        leave = attendance_records.filter(status="leave").count()
        absent = attendance_records.filter(status="absent").count()

        overtime_hours = AttendanceService.get_monthly_overtime_hours(
            attendance_records
        )

        return {
            "present_day": present_day,
            "half_day": half_day,
            "overtime_hours": overtime_hours,
            'absent':absent,
            'leave':leave
        }

    @staticmethod
    def get_monthly_overtime_hours(attendance_records: QuerySet[Attendance]) -> Decimal:
        overtime_hours = (
            attendance_records.aggregate(total=Sum("working_summary__overtime_hours"))[
                "total"
            ]
            or 0
        )

        return overtime_hours
