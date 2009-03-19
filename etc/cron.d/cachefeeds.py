#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
APP_BASE        = os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

from tweetypy import *
import tweetypy.sensitive
import pprint

pp = pprint.PrettyPrinter()

try:
    twit = TweetyPy(tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd)
except:
    raise TwitterNotAvailable

friends = twit.get_friends_timeline()
replies = twit.get_replies_to_user()

pp.pprint(friends)
pp.pprint(replies)