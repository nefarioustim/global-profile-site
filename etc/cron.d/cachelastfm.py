#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------
# Global imports
#----------------------------------------
import os
import sys

#----------------------------------------
# Register globals
#----------------------------------------

APP_BASE = os.path.join(os.path.dirname(__file__), '../..')
LIB_BASE = os.path.join(APP_BASE, 'lib')

#----------------------------------------
# Hack sys.path
#----------------------------------------

sys.path.insert(0, LIB_BASE)

import caching

caching.make_cache("lastfm", "http://ws.audioscrobbler.com/1.0/user/nefarioustim/recenttracks.rss", 5)