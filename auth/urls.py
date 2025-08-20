from django.urls import path 
from .views import LoginView,LogoutView,RefreshTokenView,ProtectedView

app_name='auth'
urlpatterns=[
   path('login/',LoginView.as_view(),name='login_view'),
   path('logout/',LogoutView.as_view(),name='logout_view'),
   path('refresh-token/',RefreshTokenView.as_view(),name='refresh_token_view'),
   path('protected-view/',ProtectedView.as_view(),name='protected_view'), 

    
]