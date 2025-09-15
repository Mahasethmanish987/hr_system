from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer
from auth.services.user_service import AuthenticationService
from auth.services.token_service import TokenService
from .exceptions import InactiveUserException,InvalidCredentialException
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings 
from datetime import datetime, timezone
from employee_module.permissions import IsAnonymousUser

  
class  LoginView(APIView):
    permission_classes = [IsAnonymousUser]
    
    def post(self,request): 
        login_serializer=LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        email=login_serializer.validated_data['username']
        password=login_serializer.validated_data["password"]

        try:
            user = AuthenticationService.authenticate_user(request, email, password)
        except InvalidCredentialException:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except InactiveUserException:
            return Response({"error": "Your email was not activated go and check email inbox for activatation"}, status=status.HTTP_403_FORBIDDEN)
        tokens=TokenService.generate_token_for_user(user)

        response=Response({
            'message':"Login successful",
            'user_id':user.id,
            'access_token':tokens['access_token'],
            'refresh_token':tokens['refresh_token'],
            'role': [user.employee.role if user.employee else None]
        },status=status.HTTP_200_OK

        )
        
        return response 
        

User=get_user_model()
class RefreshTokenView(APIView):
    permission_classes = [IsAnonymousUser]
    

    def post(self, request):
        old_refresh_token = request.data.get("refresh_token")

        # Validate input
        if not old_refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Verify old token
            old_token = RefreshToken(old_refresh_token)
            

            # Get user from token
            user_id = old_token.payload.get("user_id")
            user = User.objects.get(id=user_id, is_active=True)

            # Generate new tokens
            new_refresh = RefreshToken.for_user(user)
            new_access_token = str(new_refresh.access_token)
            new_refresh_token = str(new_refresh)

            # Get new token expiration
            new_refresh_exp = datetime.fromtimestamp(
                new_refresh.payload["exp"], tz=timezone.utc
            )

            #
            response = Response(
                {
                    "message": "Access token refreshed",
                    "refresh_token": new_refresh_token,
                    "refresh_token_exp": new_refresh_exp.isoformat(),
                    "access_token":new_access_token,
                }
            )

            
            old_token.blacklist()

            return response

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User account not found or disabled"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    

class LogoutView(APIView):
    """
    Logs out user by:
    1. Clearing access token cookie
    2. Blacklisting refresh token
    Requires: { "refresh_token": "your_refresh_token" }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle token blacklisting first
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            response=Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            return response 
        
        # Prepare success response
        response = Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
        
        # Clear access token cookie
        
        return response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Access authenticated user via request.user
        return Response({"message": f"Hello, {request.user.username}!"})
