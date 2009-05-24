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
    
    """Builds cache from Nefarious Designs feed using the caching module."""
    
    import gzipickle, caching
    from datetime import datetime
    
    if os.path.exists( CACHE_BASE + '/blog-feed.pkl' ):
        blog        = list( gzipickle.load( CACHE_BASE + '/blog-feed.pkl' ) )[0]
        etag        = blog.etag
        modified    = blog.modified
    else:
        etag        = None
        modified    = None
    
    blog = caching.get_blog_feed( etag = etag, modified = modified )
    
    if blog.status != 304:
        blog.entries    = blog.entries[:5]
        
        if blog:
            gzipickle.save( CACHE_BASE + '/blog-feed.pkl', blog )
    else:
        print "304 returned; not fetching."

if __name__ == "__main__":
    make_cache()