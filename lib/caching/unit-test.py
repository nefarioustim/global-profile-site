# -*- coding: utf-8 -*-

"""Unit test for Global Profile Site Caching module"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import caching

class CachingSuccessTest( unittest.TestCase ):
	accepted_counts = [1, 2, 5, 10, 50, 100]
	
	def test_caching_get_twitter_feed_with_no_count( self ):
		"""Caching.get_twitter_feed should return tweets when no count is passed."""
		result = caching.get_twitter_feed()
		self.assertTrue ( result )
	
	def test_caching_get_twitter_feed_with_count( self ):
		"""Caching.get_twitter_feed should return same number of tweets as count."""
		for count in self.accepted_counts:
			result = caching.get_twitter_feed( count )
			self.assertEqual( count, len( result ) )
	
	# def test_caching_get_flickr_feed( self ):
	# 	pass
	# 
	# def test_caching_get_lastfm_feed( self ):
	# 	pass
	# 
	# def test_caching_get_blog_feed( self ):
	# 	pass

class CachingFailureTest( unittest.TestCase ):
	unaccepted_counts = [-1, 0, "test"]
	pass
    
class CachingSanityTest( unittest.TestCase ):
    pass

if __name__ == "__main__":
    unittest.main()