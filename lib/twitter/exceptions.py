# -*- coding: utf-8 -*-
# Define exceptions

class TwitterError(Exception):
    """Generic parent class for exceptions"""
    pass

class TwitterNotAvailable(TwitterError):
    """Raised when Twitter is down"""
    pass

class LoginNotValid(TwitterError):
    """Raised when invalid login information is provided"""
    pass

class UserNotAuthorised(TwitterError):
    """Raised when user is not authorised to perform the action"""
    pass

class NotLoggedIn(TwitterError):
    """Raised when user isn't logged in"""
    pass

class MalformedXML(TwitterError):
    """Raised when malformed XML is returned"""
    pass