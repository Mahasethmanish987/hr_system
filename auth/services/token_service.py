from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model 
User=get_user_model()

class TokenService: 

      def generate_token_for_user(user:User)->dict: 
           """generating the refresh token and access token """     

           refresh=RefreshToken.for_user(user)

           access_token=str(refresh.access_token)
           refresh_token=str(refresh)
           return {
                 'access_token':access_token, 
                 'refresh_token':refresh_token 
           }

