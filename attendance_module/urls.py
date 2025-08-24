from django.urls import path ,include
from attendance_module.views import PunchAPIView,EmployeeOvertimeViewSet,EmployeeOvertimeApproveViewSet,AttendanceViewset
from rest_framework.routers import DefaultRouter



app_name='attendance_module'
router=DefaultRouter()
router.register(r"overtime",EmployeeOvertimeViewSet)
router.register(r"overtime-approval",EmployeeOvertimeApproveViewSet,basename='overtime-approval')
router.register(r"attendance",AttendanceViewset,basename='attendance')


urlpatterns=[
     path("", PunchAPIView.as_view(),name='punch-api'),
     path("", include(router.urls))
     
]
