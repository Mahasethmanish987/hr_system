
from django.contrib.auth import get_user_model,authenticate
from typing import Union ,Type 
from auth.exceptions import InactiveUserException,InvalidCredentialException


User=get_user_model()

class AuthenticationService:

    @staticmethod
    def authenticate_user(request,username:str,password:str)-> Union[Type[User],str,None]: 
        """authenticate the user and return the status or User"""

        user=User.objects.filter(username=username).first()
        
        if user is None: 
            raise InvalidCredentialException()
        if not   user.is_active: 
            raise InactiveUserException()
        user=authenticate(request,username=username,password=password)
        
        if not user: 
            raise InvalidCredentialException()
        
        return user 
       