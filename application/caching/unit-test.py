# -*- coding: utf-8 -*-

"""Unit test for Global Profile Site Caching module"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import caching import *

class CachingSuccessTest( unittest.TestCase ):
	accepted_values = [0, 1, 2, 5, 10, 50, 100]
	
	def test_caching_get_twitter_feed( self ):
		"""Caching.get_twitter_feed should return non-direct tweets involving authorised user."""
		for value in self.accepted_values
			result = caching.get_public_timeline( value )
			self.assertEqual( value, len( result ) )
	
	def test_caching_get_flickr_feed( self ):
		pass
	
	def test_caching_get_lastfm_feed( self ):
		pass
	
	def test_caching_get_blog_feed( self ):
		pass

class CachingFailureTest( unittest.TestCase ):
	pass
    
class CachingSanityTest( unittest.TestCase ):
    pass

if __name__ == "__main__":
    unittest.main()