# -*- coding: utf-8 -*-

import urllib2, base64
from xml.dom import minidom

# Define exceptions

class TwitterError(Exception):
    """Generic parent class for exceptions"""
    pass

class TwitterNotAvailable(TwitterError):
    """Raised when Twitter is down"""
    pass

class RateLimitExceeded(TwitterError):
    """Raised when API rate limit is exceeded"""
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

class HTTPError(TwitterError):
    """Raised for other HTTPLib errors"""
    pass

# Main abstraction class

class Twitter:
    """ Abstraction for Twitter API """
    
    logged_in   = False
    username    = None
    password    = None
    auth_string = ''
    
    # Special methods
    
    def __init__(self, username=None, password=None):
        self.username   = username
        self.password   = password
        
        if self.username and self.password:
            self.logged_in = self.__verify_login()
    
    # Private methods
    
    def __verify_login(self):
        request             = urllib2.Request('http://twitter.com/account/verify_credentials.xml')
        self.auth_string    = base64.encodestring('%s:%s' % (self.username, self.password))
        request.add_header('Authorization', 'Basic %s' % self.auth_string)
        
        try:
            results = urllib2.urlopen(request).read()
        except urllib2.HTTPError, error:
            if error.code == 401 or error.code == 403:
                raise LoginNotValid
            elif error.code == 400:
                raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
            else:
                raise HTTPError, "HTTP Error: %s (%s)" % (error.msg, error.code)
        else:
            return True
    
    def __authorised_get(self, url):
        if not self.logged_in:
            raise NotLoggedIn
        
        request = urllib2.Request(url)
        request.add_header('Authorization', 'Basic %s' % self.auth_string)
        
        try:
            results = urllib2.urlopen(request).read()
        except urllib2.HTTPError, error:
            if error.code == 401 or error.code == 403:
                raise UserNotAuthorised, "This user is not authorised for this action (%s)" % error.code
            elif error.code == 400:
                raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
            else:
                raise HTTPError, "HTTP Error: %s (%s)" % (error.msg, error.code)
        else:
            return results
    
    def __anonymous_get(self, url):
        request = urllib2.Request(url)
        
        try:
            results = urllib2.urlopen(request).read()
        except urllib2.HTTPError, error:
            if error.code == 400:
                raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
            else:
                raise HTTPError, "HTTP Error: %s (%s)" % (error.msg, error.code)
        else:
            return results
    
    def __parse_messages(self, messages):
        try:
            node = minidom.parseString(messages)
        except:
            raise MalformedXML
        else:
            return [self.__parse_message(message.toxml("utf-8")) for message in node.getElementsByTagName('status')]
    
    def __parse_message(self, message):
        try:
            node = minidom.parseString(message)
        except:
            raise MalformedXML
        else:
            result = {
                'id' : node.getElementsByTagName('id')[0].firstChild.data,
                'created_at' : node.getElementsByTagName('created_at')[0].firstChild.data,
                'text' : node.getElementsByTagName('text')[0].firstChild.data,
                'user' : self.__parse_user(node.getElementsByTagName('user')[0].toxml("utf-8"))
            }

            return result
    
    def __parse_user(self, user):
        try:
            node = minidom.parseString(user)
        except:
            raise MalformedXML
        else:
            result = {
                'id' : node.getElementsByTagName('id')[0].firstChild.data,
                'name' : node.getElementsByTagName('name')[0].firstChild and node.getElementsByTagName('name')[0].firstChild.data,
                'screen_name' : node.getElementsByTagName('screen_name')[0].firstChild.data,
                'location' : node.getElementsByTagName('location')[0].firstChild and node.getElementsByTagName('location')[0].firstChild.data,
                'description' : node.getElementsByTagName('description')[0].firstChild and node.getElementsByTagName('description')[0].firstChild.data,
                'profile_image_url' : node.getElementsByTagName('profile_image_url')[0].firstChild.data,
                'url' : node.getElementsByTagName('url')[0].firstChild and node.getElementsByTagName('url')[0].firstChild.data
            }

            return result
    
    # Public Methods
    
    def get_public_timeline(self):
        response = self.__anonymous_get('http://twitter.com/statuses/public_timeline.xml')
        return self.__parse_messages(response)
    
    def get_user_timeline(self):
        response = self.__authorised_get('http://twitter.com/statuses/user_timeline.xml')
        return self.__parse_messages(response)
    
    def get_replies_to_user(self):
        return False