# -*- coding: utf-8 -*-

class TwitterError(Exception):
    """Generic parent class for exceptions"""
    pass

class UserNotAuthorized(TwitterError):
    """Raised when user is not able to perform the action"""
    pass