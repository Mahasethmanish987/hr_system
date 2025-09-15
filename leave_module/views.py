from rest_framework import viewsets 
from rest_framework import permissions
from .models import LeaveRequest,LeaveBalance
from .serializers import LeaveRequestSerializer,LeaveRequestStatusUpdateSerializer,LeaveBalanceUpdateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone 
from rest_framework import status
from employee_module.permissions import IsHrOrSuperUser
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from employee_module.permissions import IsHrOrSuperUser ,check_hr,check_manager,check_normal_employee
from .filters import LeaveRequestFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q 

class LeaveRequestViewSet(viewsets.ModelViewSet): 

    queryset=LeaveRequest.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=LeaveRequestSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=LeaveRequestFilter 
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or check_hr(self.request):
            return LeaveRequest.objects.all()

        elif hasattr(user, "employee") and check_manager(self.request):
            return LeaveRequest.objects.filter(
                employee__reporting_manager=user.employee
            ) | LeaveRequest.objects.filter(employee__user=user)
        elif hasattr(user, "employee"):
            leave_queryset = LeaveRequest.objects.filter(employee__user=user)
            
            return leave_queryset 
        else:
            return LeaveRequest.objects.none()

    def get_serializer_class(self): 

        if self.action in ['update_status']:
            return LeaveRequestStatusUpdateSerializer
        return LeaveRequestSerializer
    
    @action(detail=True,methods=['patch'],url_path='update-status',permission_classes=[IsHrOrSuperUser])
    def update_status(self,request,pk=None): 
        leave_request=self.get_object()
        serializer=self.get_serializer(leave_request,data=request.data,context={'request':request},partial=True)

        try: 
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e: 
            return Response({"error":e.detail},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

class LeaveBalanceViewSet(viewsets.ModelViewSet):
    queryset=LeaveBalance.objects.all()
    permission_classes=[IsHrOrSuperUser]
    serializer_class=LeaveBalanceUpdateSerializer
    http_method_names = ["get","put", "patch"]

