#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

APP_BASE		= os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE		= os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

import getopt
import pprint
from tweetypy import *
import tweetypy.sensitive

def make_cache( argv ):
	try:
		opts, args = getopt.getopt( argv, "l:", ["limit="] )
	except getopt.GetoptError, err:
		print str(err)
		sys.exit()
		
	try:
		twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
	except:
		raise TwitterNotAvailable

	user		= twit.get_user_timeline( 5 )
	replies		= twit.get_replies_to_user( 5 )
	combined	= user + replies
	combined.sort( lambda x, y: cmp( x["created_at"], y["created_at"] ) )
	combined.reverse
	
	return combined

if __name__ == "__main__":
	stuff = make_cache( sys.argv[1:] )
	
	# For debug
	pp = pprint.PrettyPrinter()
	pp.pprint( stuff )