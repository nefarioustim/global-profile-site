#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit test for Global Profile Site Caching module"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import caching

class CachingSuccessTest( unittest.TestCase ):
	accepted_counts = [ 1, 2, 5, 10 ]
	
	def test_caching_get_twitter_feed_with_no_count( self ):
		"""Caching.get_twitter_feed should return tweets when no count is passed."""
		result = caching.get_twitter_feed()
		self.assertTrue ( result )
	
	def test_caching_get_twitter_feed_with_count( self ):
		"""Caching.get_twitter_feed should return tweets when count is passed."""
		for count in self.accepted_counts:
			result = caching.get_twitter_feed( count )
			self.assertTrue( result )
	
	def test_caching_get_blog_feed( self ):
		"""Caching.get_blog_feed should return a feed"""
		result = caching.get_blog_feed()
		self.assertTrue( result )

class CachingFailureTest( unittest.TestCase ):
	unaccepted_counts = [ -1, 0, "test" ]
	
	def test_caching_get_twitter_feed_with_count( self ):
		"""Caching.get_twitter_feed should fail with bad count."""
		for count in self.unaccepted_counts:
			self.assertRaises( caching.CountNotValid, caching.get_twitter_feed, count)
    
class CachingSanityTest( unittest.TestCase ):
	accepted_counts = [ 1, 2, 5, 10 ]
	
	def test_caching_get_twitter_feed_with_count( self ):
		"""Caching.get_twitter_feed should return same number of tweets as count."""
		for count in self.accepted_counts:
			result = caching.get_twitter_feed( count )
			self.assertEqual( count, len( result[0] ) )
			self.assertEqual( count, len( result[1] ) )

if __name__ == "__main__":
    unittest.main()