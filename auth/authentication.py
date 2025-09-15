from rest_framework_simplejwt.authentication import JWTAuthentication 

class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self,request): 
        print("cookie called")
        raw_token = request.COOKIES.get("access_token")
        print(raw_token)
        if raw_token is None:
            header = self.get_header(request)
            if header is not None:
                raw_token = self.get_raw_token(header)

       
        if raw_token is None:
            print('no raw_token')
            return None

        
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
