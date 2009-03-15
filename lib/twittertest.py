# -*- coding: utf-8 -*-

"""Unit test for Twitter module"""

from twitter import Twitter
import unittest
import sensitive

class TwitterSuccessTest(unittest.TestCase):                    
    def test_get_public_timeline(self):
        """Twitter.get_public_timeline should return messages from the public timeline"""
        twittertest = Twitter()
        response = twittertest.get_public_timeline()
        # Not sure what needs to be asserted here. Will need more logic.
        self.assertTrue(response)
    
    def test_get_user_timeline(self):
        """Twitter.get_user_timeline should return messages from the user timeline"""
        twittertest = Twitter()
        response = twittertest.get_user_timeline()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue(response)
    
    def test_get_replies_to_user(self):
        """Twitter.get_replies_to_user should return @ reply messages to the user"""
        twittertest = Twitter()
        response = twittertest.get_replies_to_user()
        # Similar to above; not sure what needs to be asserted.
        self.assertTrue(response)

class TwitterFailureTest(unittest.TestCase):
    pass
    
class TwitterSanityTest(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
