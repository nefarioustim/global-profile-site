# -*- coding: utf-8 -*-

""" Feed caching for Global Profile Site """

# Define exceptions

class CachingError( Exception ):
    """Generic parent class for exceptions"""
    pass

class CountNotValid( CachingError ):
    """Invalid value was passed as count"""
    pass

def _test_count( count ):
    if count != None:
        try:
            count = int( count )
        except:
            raise CountNotValid
        else:
            if count < 1:
                raise CountNotValid

#----------------------------------------
def get_twitter_feed( count=None, etag=None ):
    _test_count( count )
    
    from tweetypy import TweetyPy, TwitterNotAvailable
    import tweetypy.sensitive
    
    try:
        twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
    except:
        raise TwitterNotAvailable
        
    user        = twit.get_user_timeline( count, etag )
    replies     = twit.get_replies_to_user( count, etag )
    
    return ( user, replies, twit.etag )
#----------------------------------------

# Needs refactoring.

#----------------------------------------
def get_blog_feed( etag = None, modified = None ):
    import feedparser
    
    return feedparser.parse( r"http://feeds2.feedburner.com/nefariousdesigns", etag = etag, modified = modified )
#----------------------------------------

#----------------------------------------
def get_flickr_feed( etag = None, modified = None ):
    import feedparser
    
    return feedparser.parse( r"http://api.flickr.com/services/feeds/photos_public.gne?id=27203808@N00&lang=en-gb&format=atom", etag = etag, modified = modified )
#----------------------------------------

#----------------------------------------
def get_lastfm_feed( etag = None, modified = None ):
    import feedparser
    
    return feedparser.parse( r"http://ws.audioscrobbler.com/1.0/user/nefarioustim/recenttracks.rss", etag = etag, modified = modified )
#----------------------------------------