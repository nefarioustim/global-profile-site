# -*- coding: utf-8 -*-

class TwitterError(Exception):
    """Generic parent class for exceptions"""
    pass
    
class LoginNotValid(TwitterError):
    """Raised when invalid login information is provided"""
    pass

class UserNotAuthorised(TwitterError):
    """Raised when user is not authorised to perform the action"""
    pass