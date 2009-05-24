#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------
# Global imports
#----------------------------------------
import os, sys

#----------------------------------------
# Register globals
#----------------------------------------

APP_BASE        = os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )
CACHE_BASE      = os.path.join( APP_BASE, 'var/cache' )
TWITTER_COUNT   = 5

#----------------------------------------
# Hack sys.path
#----------------------------------------

sys.path.insert( 0, LIB_BASE )

def make_cache():
    
    """Builds cache from Twitter feeds using the caching module."""
    
    import gzipickle, caching
    from datetime import datetime
    
    if os.path.exists( CACHE_BASE + '/twit-etag.pkl' ):
        etag    = list( gzipickle.load( CACHE_BASE + '/twit-etag.pkl' ) )[0]
    else:
        etag = None
    
    user, replies, etag = caching.get_twitter_feed( TWITTER_COUNT, etag )
    
    if user:
        gzipickle.save( CACHE_BASE + '/twit-user.pkl', user )
    
    if replies:
        gzipickle.save( CACHE_BASE + '/twit-reply.pkl', replies )
    
    if etag:
        gzipickle.save( CACHE_BASE + '/twit-etag.pkl', etag )

if __name__ == "__main__":
    make_cache()