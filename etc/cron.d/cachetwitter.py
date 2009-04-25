#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------
# Global imports
#----------------------------------------
import os, sys

#----------------------------------------
# Register globals
#----------------------------------------

APP_BASE		= os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE		= os.path.join( APP_BASE, 'lib' )
CACHE_BASE		= os.path.join( APP_BASE, 'var/cache' )
TWITTER_COUNT	= 5

#----------------------------------------
# Hack sys.path
#----------------------------------------

sys.path.insert( 0, LIB_BASE )

#----------------------------------------
def make_cache():
#----------------------------------------

	"""Builds cache from Twitter feeds using the caching module."""

	import pickle, caching
	from datetime import datetime
	
	if os.path.exists( CACHE_BASE + '/twit-etag.pkl' ):
		cache	= open( CACHE_BASE + '/twit-etag.pkl', 'rb' )
		etag	= pickle.load( cache )
		cache.close()
	else:
		etag = None
	
	user, replies, etag = caching.get_twitter_feed( TWITTER_COUNT, etag )
	
	if user:
		cache = open( CACHE_BASE + '/twit-user.pkl', 'wb' )
		pickle.dump( user, cache )
		cache.close()
	
	if replies:
		cache = open( CACHE_BASE + '/twit-reply.pkl', 'wb' )
		pickle.dump( replies, cache )
		cache.close()
	
	if etag:
		cache = open( CACHE_BASE + '/twit-etag.pkl', 'wb' )
		pickle.dump( etag, cache )
		cache.close()

#----------------------------------------
# Main
#----------------------------------------

if __name__ == "__main__":
	make_cache()