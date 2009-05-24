# -*- coding: utf-8 -*-

""" Feed caching for Global Profile Site """

#----------------------------------------
# Global imports
#----------------------------------------
import os

#----------------------------------------
# Register globals
#----------------------------------------

APP_BASE = os.path.join(os.path.dirname(__file__), '../..')
CACHE_BASE = os.path.join(APP_BASE, 'var/cache')

#----------------------------------------
# Define exceptions
#----------------------------------------

class CachingError(Exception):
    """Generic parent class for exceptions"""
    pass

class CountNotValid(CachingError):
    """Invalid value was passed as count"""
    pass

#----------------------------------------
# Functions
#----------------------------------------

def _test_count(count):
    if count != None:
        try:
            count = int(count)
        except:
            raise CountNotValid
        else:
            if count < 1:
                raise CountNotValid

def get_twitter_feed(count=None, etag=None):
    _test_count(count)
    
    from tweetypy import TweetyPy, TwitterNotAvailable
    import tweetypy.sensitive
    
    try:
        twit = TweetyPy(tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd)
    except:
        raise TwitterNotAvailable
        
    user = twit.get_user_timeline(count, etag)
    replies = twit.get_replies_to_user(count, etag)
    
    return (user, replies, twit.etag)

def get_feed(url, count=None, etag=None, modified=None):
    _test_count(count)
    
    import feedparser
    
    feed = feedparser.parse(url, etag=etag, modified=modified)
    
    if feed.status != 304 and count != None:
        feed.entries = feed.entries[:count]
    
    return feed

def make_cache(name, url, count=None):
    
    """Builds cache from feed using the universal feeds parser."""
    
    _test_count(count)
    
    import gzipickle
    from datetime import datetime
    
    path = os.path.join(CACHE_BASE, name + '-feed.pkl')
    
    if os.path.exists(path):
        feed = list(gzipickle.load(path))[0]
        etag = feed.etag
        modified = feed.modified
    else:
        etag = None
        modified = None
    
    feed = get_feed(url, count, etag=etag, modified=modified)
    
    if feed.status != 304:
        gzipickle.save(path, feed)
    else:
        print "304 returned; not fetching."