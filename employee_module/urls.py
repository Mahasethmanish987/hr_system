from django.urls import include, path
from rest_framework.routers import DefaultRouter

from employee_module.views import (
    DepartmentViewSet,
    EmployeeHistoryViewSet,
    EmployeeStatusViewSet,
    EmployeeTypeViewSet,
    EmployeeViewSet,
    JobTitleViewSet,
    EmergencyContactViewset,
    EmployeeProfileViewSet
)

app_name = "employee_module"


router = DefaultRouter()
router.register(r"employee-types", EmployeeTypeViewSet)
router.register(r"employee-status", EmployeeStatusViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"job-title", JobTitleViewSet)
router.register(r"employee", EmployeeViewSet)
router.register(r"employee-history", EmployeeHistoryViewSet)
router.register(r"employee-contact", EmergencyContactViewset)
router.register(r"employee-profile",EmployeeProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
