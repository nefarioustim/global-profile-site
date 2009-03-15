# -*- coding: utf-8 -*-

import urllib2
import exceptions

class Twitter:
    """ Abstraction for Twitter API """
    
    logged_in   = False
    username    = None
    password    = None
    
    def __init__(self, username=None, password=None):
        self.username   = username
        self.password   = password
    
    def __login(self, username, password):
        self.logged_in  = True
    
    def __authorised_get(self, url):
        pass
    
    def __anonymous_get(self, url):
        request = urllib2.Request(url)
        results = urllib2.urlopen(request).read()
        return results
    
    def get_public_timeline(self):
        return False
    
    def get_user_timeline(self):
        return False
    
    def get_replies_to_user(self):
        return False