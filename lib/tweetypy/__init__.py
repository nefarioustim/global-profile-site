# -*- coding: utf-8 -*-

import urllib2, base64
from xml.dom import minidom

# Define exceptions

class TweetyPyError(Exception):
    """Generic parent class for exceptions"""
    pass

class TwitterNotAvailable(TweetyPyError):
    """Raised when Twitter is down"""
    pass

class RateLimitExceeded(TweetyPyError):
    """Raised when API rate limit is exceeded"""
    pass

class LoginNotValid(TweetyPyError):
    """Raised when invalid login information is provided"""
    pass

class UserNotAuthorised(TweetyPyError):
    """Raised when user is not authorised to perform the action"""
    pass

class NotLoggedIn(TweetyPyError):
    """Raised when user isn't logged in"""
    pass

class MalformedXML(TweetyPyError):
    """Raised when malformed XML is returned"""
    pass

class HTTPError(TweetyPyError):
    """Raised for other HTTPLib errors"""
    pass

# Main abstraction class

class TweetyPy:
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
            def get_tag(tag):
                return node.getElementsByTagName(tag)[0].firstChild and node.getElementsByTagName(tag)[0].firstChild.data
            
            result = {
                'id' : get_tag('id'),
                'name' : get_tag('name'),
                'screen_name' : get_tag('screen_name'),
                'location' : get_tag('location'),
                'description' : get_tag('description'),
                'profile_image_url' : get_tag('profile_image_url'),
                'url' : get_tag('url'),
            }

            return result
    
    # Public Methods
    
    def get_public_timeline(self):
        response = self.__anonymous_get('http://twitter.com/statuses/public_timeline.xml')
        return self.__parse_messages(response)
    
    def get_user_timeline(self):
        response = self.__authorised_get('http://twitter.com/statuses/user_timeline.xml')
        return self.__parse_messages(response)
    
    def get_friends_timeline(self):
        response = self.__authorised_get('http://twitter.com/statuses/friends_timeline.xml')
        return self.__parse_messages(response)
    
    def get_replies_to_user(self):
        response = self.__authorised_get('http://twitter.com/statuses/replies.xml')
        return self.__parse_messages(response)