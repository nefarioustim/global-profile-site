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

caching.make_cache("flickr", "http://api.flickr.com/services/feeds/photos_public.gne?id=27203808@N00&lang=en-gb&format=atom")