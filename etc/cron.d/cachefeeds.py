#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

APP_BASE        = os.path.join( os.path.dirname( __file__ ), '../..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )

sys.path.insert( 0, LIB_BASE )

import pprint
from tweetypy import *
import tweetypy.sensitive

def makecache( argv ):
    try:
        opts, args = getopt.getopt( argv, "l:", ["limit="] )
    except getopt.GetoptError:
        
        
    try:
        twit = TweetyPy( tweetypy.sensitive.twitter_user, tweetypy.sensitive.twitter_passwd )
    except:
        raise TwitterNotAvailable

    user    = twit.get_user_timeline()
    replies = twit.get_replies_to_user()

    # For debug
    pp = pprint.PrettyPrinter()
    pp.pprint( user )
    pp.pprint( replies )

if __name__ == "__main__":
    makecache( sys.argv[1:] )