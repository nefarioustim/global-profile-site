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

def get_twitter_feed( count=None, etag=None ):
	_test_count( count )
	
	from tweetypy import TweetyPy, TwitterNotAvailable
	import tweetypy.sensitive
	
	try:
		twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
	except:
		raise TwitterNotAvailable
		
	user		= twit.get_user_timeline( count, etag )
	replies		= twit.get_replies_to_user( count, etag )
	
	return ( user, replies, twit.etag )
	
def get_blog_feed():
	import feedparser
	
	return feedparser.parse( "http://feeds2.feedburner.com/nefariousdesigns" )