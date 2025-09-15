from datetime import date

import pytest
from leave_module.factories import LeaveRequestFactory
from leave_module.services.leave_services import LeaveRequestService

@pytest.mark.parametrize("starting_date,ending_date,expected_approved_days",
                         [(date(2025, 8, 1),date(2025, 8, 31),4),
                          (date(2025, 9, 1),date(2025,9,30),9)])
def test_leave_approval_days(db, test_employee, leave_request_conftest,starting_date,ending_date,expected_approved_days):
    

    approved_days = LeaveRequestService.get_approved_leave(
        test_employee.id, starting_date, ending_date
    )
    assert approved_days == expected_approved_days


@pytest.mark.parametrize(
    "test_date,leave_exists",
    [
        (date(2025, 8, 1), True),
        (date(2025, 8, 10), True),
        (date(2025, 8, 11), True),
        (date(2025, 8, 31), True),
        (date(2025, 8, 20), False),
        (date(2025, 8, 21), False),
    ],
)
def test_check_leave(
    db, test_employee, leave_request_conftest, test_date, leave_exists
):
    assert leave_exists == LeaveRequestService.check_leave_approval(
        test_employee.id, test_date
    )


@pytest.mark.parametrize("start_date,end_date,approval_date,leave_counted_days",
                         [(date(2025,8,9),date(2025,8,11),date(2025,8,7),2),
                         (date(2025,7,29),date(2025,8,4),date(2025,7,27),6),
                          ])
def test_leave_days_count(db, test_employee, test_hr,start_date,end_date,approval_date,leave_counted_days):
    
    LeaveRequestFactory.create(
        employee=test_employee,
        start_date=start_date,
        end_date=end_date,
        approved_by=test_hr,
        approved_date=approval_date,
        status="approved",
    )

    assert leave_counted_days==LeaveRequestService.calculate_leave_days(start_date,end_date)
