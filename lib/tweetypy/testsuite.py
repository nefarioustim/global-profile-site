#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit test for Twitter module"""

import os, sys
sys.path.insert( 0, os.path.join( os.path.dirname( __file__ ), '..' ) )

from tweetypy import *
import sensitive
import unittest

class TweetyPySuccessTest( unittest.TestCase ):
    def test_get_public_timeline( self ):
        """TweetyPy.get_public_timeline should return messages from the public timeline"""
        twittertest = TweetyPy()
        response = twittertest.get_public_timeline()
        # Not sure what needs to be asserted here. Will need more logic.
        self.assertTrue( response )
    
    def test_get_user_timeline( self ):
        """TweetyPy.get_user_timeline should return messages from the user timeline"""
        twittertest = TweetyPy( sensitive.twitter_user, sensitive.twitter_passwd )
        response = twittertest.get_user_timeline()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue( response )
    
    def test_get_friends_timeline( self ):
        """TweetyPy.get_user_timeline should return messages from the user timeline"""
        twittertest = TweetyPy( sensitive.twitter_user, sensitive.twitter_passwd )
        response = twittertest.get_friends_timeline()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue( response )
    
    def test_get_replies_to_user( self ):
        """TweetyPy.get_replies_to_user should return @ reply messages to the user"""
        twittertest = TweetyPy( sensitive.twitter_user, sensitive.twitter_passwd )
        response = twittertest.get_replies_to_user()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue( response )

class TweetyPyFailureTest( unittest.TestCase ):
    bad_user = {
        'username': 'thisuserdoesnotexist',
        'password': 'thisisnotarealpassword'
    }
    
    def test_user_validation( self ):
        """Twitter instantiation should fail with bad credentials"""
        self.assertRaises( LoginNotValid, TweetyPy, self.bad_user[ 'username' ], self.bad_user[ 'password' ] )
    
class TweetyPySanityTest( unittest.TestCase ):
    pass

if __name__ == "__main__":
    unittest.main()
