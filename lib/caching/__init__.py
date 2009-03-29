# -*- coding: utf-8 -*-

""" Feed caching for Global Profile Site """

def get_twitter_feed( count=None ):
	from tweetypy import TweetyPy, TwitterNotAvailable
	import tweetypy.sensitive
	
	try:
		twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
	except:
		raise TwitterNotAvailable
		
	user		= twit.get_user_timeline( count )
	replies		= twit.get_replies_to_user( count )
	combined	= user + replies
	combined.sort( lambda x, y: cmp( x["created_at"], y["created_at"] ) )
	combined.reverse()
	return combined[:count]