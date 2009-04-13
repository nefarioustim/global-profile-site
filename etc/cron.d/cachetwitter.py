#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

APP_BASE		= os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE		= os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

import caching

TWITTER_CACHE_FILE = "/var/www/timhuegdon.com/var/cache/twitter.pkl"
TWITTER_COUNT = 5

def make_cache():
	import pickle
	from datetime import datetime
	
	last_modified = datetime.fromtimestamp( os.stat( TWITTER_CACHE_FILE ).st_mtime )
	
	tweets = caching.get_twitter_feed( TWITTER_COUNT, last_modified )
	
	cache = open( TWITTER_CACHE_FILE, 'wb' )
	pickle.dump( tweets, cache )	
	cache.close()

if __name__ == "__main__":
	make_cache()