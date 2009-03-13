# -*- coding: utf-8 -*-

import urllib, urllib2

class Twitter:
    """ Abstraction for Twitter API """
    
    logged_in   = False
    username    = None
    password    = None
    
    def __init__(self, username=None, password=None):
        pass
    
    def __login(self, username, password):
        self.logged_in  = True
        self.username   = username
        self.password   = password
    
    def __authorised_get(self, url):
        pass
    
    def __anonymous_get(self, url):
        request = urllib2.Request(url)
        results = urllib2.urlopen(request).read()
        return results