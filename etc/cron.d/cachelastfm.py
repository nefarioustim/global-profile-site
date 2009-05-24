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

#----------------------------------------
# Hack sys.path
#----------------------------------------

sys.path.insert( 0, LIB_BASE )

def make_cache():
    
    """Builds cache from last.fm feed using the caching module."""
    
    import gzipickle, caching
    from datetime import datetime
    
    if os.path.exists( CACHE_BASE + '/lastfm-feed.pkl' ):
        lastfm      = list( gzipickle.load( CACHE_BASE + '/lastfm-feed.pkl' ) )[0]
        etag        = lastfm.etag
        modified    = lastfm.modified
    else:
        etag        = None
        modified    = None
    
    lastfm = caching.get_lastfm_feed( etag = etag, modified = modified )
    
    if lastfm.status != 304:
        lastfm.entries    = lastfm.entries[:5]
        
        if lastfm:
            gzipickle.save( CACHE_BASE + '/lastfm-feed.pkl', lastfm )
    else:
        print "304 returned; not fetching."

if __name__ == "__main__":
    make_cache()