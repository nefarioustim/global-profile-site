#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

APP_BASE		= os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE		= os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

def get_twitter_feed( limit ):
	from tweetypy import *
	import tweetypy.sensitive
	
	try:
		twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
	except:
		raise TwitterNotAvailable

	user		= twit.get_user_timeline( limit )
	replies		= twit.get_replies_to_user( limit )
	combined	= user + replies
	combined.sort( lambda x, y: cmp( x["created_at"], y["created_at"] ) )
	combined.reverse()
	return combined[:limit]

def make_cache( argv ):
	import getopt
	import pickle
	
	try:
		opts, args = getopt.getopt( argv, "l:", ["limit="] )
	except getopt.GetoptError, err:
		print str(err)
		sys.exit()

	for opt, arg in opts:
		if opt == "-l":
			limit = int( arg )
	
	cache_file = args[0]
	
	tweets = get_twitter_feed( limit )
	
	cache = open(cache_file, 'wb')

	pickle.dump(tweets, cache)
	
	cache.close()

if __name__ == "__main__":
	make_cache( sys.argv[1:] )