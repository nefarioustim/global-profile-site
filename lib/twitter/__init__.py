# -*- coding: utf-8 -*-

import urllib2
from xml.dom import minidom
import exceptions

class Twitter:
    """ Abstraction for Twitter API """
    
    logged_in   = False
    username    = None
    password    = None
    
    def __init__(self, username=None, password=None):
        self.username   = username
        self.password   = password
    
    def __authorised_get(self, url):
        pass
    
    def __anonymous_get(self, url):
        request = urllib2.Request(url)
        results = urllib2.urlopen(request).read()
        return results
    
    def __parse_messages(self, messages):
        try:
            node = minidom.parseString(messages)
        except:
            raise MalformedXML

        return [self.__parse_message(message.toxml("utf-8")) for message in node.getElementsByTagName('status')]
    
    def __parse_message(self, message):
        try:
            node = minidom.parseString(message)
        except:
            # bad XML
            raise MalformedXML

        # parse out data
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
            # bad XML
            raise MalformedXML

        # parse out data
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
    
    def get_public_timeline(self):
        response = self.__anonymous_get('http://twitter.com/statuses/public_timeline.xml')
        return self.__parse_messages(response)
    
    def get_user_timeline(self):
        return False
    
    def get_replies_to_user(self):
        return False
    
    def login(self, username, password):
        self.logged_in  = True