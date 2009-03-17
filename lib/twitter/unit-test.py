# -*- coding: utf-8 -*-

"""Unit test for Twitter module"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import twitter
import sensitive
import unittest

class TwitterSuccessTest(unittest.TestCase):
    def test_get_public_timeline(self):
        """Twitter.get_public_timeline should return messages from the public timeline"""
        twittertest = twitter.Twitter()
        response = twittertest.get_public_timeline()
        # Not sure what needs to be asserted here. Will need more logic.
        self.assertTrue(response)
    
    def test_get_user_timeline(self):
        """Twitter.get_user_timeline should return messages from the user timeline"""
        twittertest = twitter.Twitter(sensitive.twitter_user, sensitive.twitter_passwd)
        response = twittertest.get_user_timeline()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue(response)
    
    def test_get_friends_timeline(self):
        """Twitter.get_user_timeline should return messages from the user timeline"""
        twittertest = twitter.Twitter(sensitive.twitter_user, sensitive.twitter_passwd)
        response = twittertest.get_friends_timeline()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue(response)
    
    def test_get_replies_to_user(self):
        """Twitter.get_replies_to_user should return @ reply messages to the user"""
        twittertest = twitter.Twitter(sensitive.twitter_user, sensitive.twitter_passwd)
        response = twittertest.get_replies_to_user()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue(response)

class TwitterFailureTest(unittest.TestCase):
    bad_user = {
        'username': 'thisuserdoesnotexist',
        'password': 'thisisnotarealpassword'
    }
    
    def test_user_validation(self):
        """Twitter instantiation should fail with bad credentials"""
        self.assertRaises( twitter.LoginNotValid, twitter.Twitter, self.bad_user['username'], self.bad_user['password'] )
    
class TwitterSanityTest(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
