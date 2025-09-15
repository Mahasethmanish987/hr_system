from employee_module.models import Employee


class EmployeeDataService:
    @staticmethod
    def get_employee_payment_detail(employee_id: id) -> dict:
        employee = (
            Employee.objects.filter(id=employee_id)
            .prefetch_related("overtime_rate")
            .first()
        )
        if not employee:
            return
        return {
            "overtime_hour_rate": employee.overtime_rate.overtime_rate,
            "salary": employee.current_salary,
            "marital_status": employee.marital_status,
        }
    @staticmethod
    def get_all_employee_ids() -> list[int]:
        return list(
            Employee.objects.filter(is_active=True).values_list("id", flat=True)
        )
    
    @staticmethod 
    def get_employees_without_salary(target_month, target_year) -> list[int]:
        return list(
            Employee.objects.filter(is_active=True).exclude(
                salary__month=target_month, salary__year=target_year
            )
        .values_list("id", flat=True))
    
