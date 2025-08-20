
class InvalidCredentialException(Exception):
    """ Raise exception when credentials does not match"""
    pass 


class InactiveUserException(Exception): 
    """ Raise exception when user is not active """
    pass 