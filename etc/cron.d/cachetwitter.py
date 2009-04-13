#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

APP_BASE		= os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE		= os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

import caching

TWITTER_CACHE_PATH = "/var/www/timhuegdon.com/var/cache/"
TWITTER_COUNT = 5

def make_cache():
	import pickle
	from datetime import datetime
	
	if os.path.exists( TWITTER_CACHE_PATH + 'twit-etag.pkl' ):
		cache = open( TWITTER_CACHE_PATH + 'twit-etag.pkl', 'rb' )
		etag = pickle.load( cache )
		cache.close()
	else:
		etag = None
	
	user, replies, etag = caching.get_twitter_feed( TWITTER_COUNT, etag )
	
	if user:
		cache = open( TWITTER_CACHE_PATH + 'twit-user.pkl', 'wb' )
		pickle.dump( user, cache )
		cache.close()
	
	if replies:
		cache = open( TWITTER_CACHE_PATH + 'twit-reply.pkl', 'wb' )
		pickle.dump( replies, cache )
		cache.close()
	
	if etag:
		cache = open( TWITTER_CACHE_PATH + 'twit-etag.pkl', 'wb' )
		pickle.dump( etag, cache )
		cache.close()

if __name__ == "__main__":
	make_cache()