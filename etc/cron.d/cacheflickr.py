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
    
    """Builds cache from Flickr feed using the caching module."""
    
    import gzipickle, caching
    from datetime import datetime
    
    if os.path.exists( CACHE_BASE + '/flickr-feed.pkl' ):
        flickr      = list( gzipickle.load( CACHE_BASE + '/flickr-feed.pkl' ) )[0]
        etag        = flickr.etag
        modified    = flickr.modified
    else:
        etag        = None
        modified    = None
    
    flickr = caching.get_flickr_feed( etag = etag, modified = modified )
    
    if flickr.status != 304:
        flickr.entries    = flickr.entries[:5]
        
        if flickr:
            gzipickle.save( CACHE_BASE + '/flickr-feed.pkl', flickr )
    else:
        print "304 returned; not fetching."

if __name__ == "__main__":
    make_cache()