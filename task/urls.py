from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,SubTaskViewSet,OnboardingOffboardingTaskViewSet
from django.urls import path ,include 

app_name='task'

router=DefaultRouter()
router.register(r"task",TaskViewSet)
router.register(r"sub-task",SubTaskViewSet)
router.register(r"employee-task",OnboardingOffboardingTaskViewSet)


urlpatterns=[
    path('',include(router.urls))
]