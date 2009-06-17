# -*- coding: utf-8 -*-

#----------------------------------------
# Global imports
#----------------------------------------

import os
import sys

#----------------------------------------
# Register constants
#----------------------------------------

APP_BASE = os.path.join(os.path.dirname(__file__), '..')
LIB_BASE = os.path.join(APP_BASE, 'lib')
TEMPLATES_BASE = os.path.join(APP_BASE, 'templates')
DATE_FORMAT = "%H:%M on %d %b %Y"

#----------------------------------------
# Hack sys.path
#----------------------------------------

sys.path.insert(0, LIB_BASE)

#----------------------------------------
# Core
#----------------------------------------

import datetime
import gzipickle
import pytz
from pytz import timezone
from newf import Application, Response, ResponseRedirect
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(TEMPLATES_BASE))

utc = pytz.utc
london = timezone('Europe/London')

def root(request):
    import re
    
    # Load feeds
    
    feeds = {
        "blog": list(gzipickle.load(os.path.join(APP_BASE, 'var/cache/blog-feed.pkl')))[0].entries,
        "flickr": list(gzipickle.load(os.path.join(APP_BASE, 'var/cache/flickr-feed.pkl')))[0].entries,
        "lastfm": list(gzipickle.load(os.path.join(APP_BASE, 'var/cache/lastfm-feed.pkl')))[0].entries,
        "twit_user": list(gzipickle.load(os.path.join(APP_BASE, 'var/cache/twit-user.pkl')))[0],
        "twit_replies": list(gzipickle.load(os.path.join(APP_BASE, 'var/cache/twit-reply.pkl')))[0],
    }
    
    # Prep feeds for output
    
    for k, feed in feeds.iteritems():
        for entry in feed:
            entry["feed"] = k
    
    def get_comp_value(d):
        f = d["feed"]

        if f == "lastfm":
            r = d["updated_parsed"]
        elif f == "twit_user" or f == "twit_replies":
            r = d["created_tuple"]
        else:
            r = d["published_parsed"]
        return r
    
    # Munge twitter feeds
    
    combined = feeds["twit_user"] + feeds["twit_replies"]
    combined.sort(lambda x, y: cmp(x["created_at"], y["created_at"]))
    combined.reverse()
    length = max(len(feeds["twit_user"]), len(feeds["twit_replies"]))
    tweets = combined[:length]
    
    for tweet in tweets:
        tweet["text"] = re.sub(r'http://([\w.\-/?#&;]+)', r"""<a href="http://\1">http://\1</a>""", tweet["text"])
        tweet["text"] = re.sub(r'@(\w+)', r"""<a href="http://twitter.com/\1/">@\1</a>""", tweet["text"])
        tweet["created_at_f"] = tweet["created_at"].strftime(DATE_FORMAT)
        tweet["created_tuple"] = tweet["created_at"].timetuple()
    
    for entry in feeds["lastfm"]:
        entry["updated"] = datetime.datetime(tzinfo=utc, *entry["updated_parsed"][:6]).astimezone(london)
        entry["updated_f"] = entry["updated"].strftime(DATE_FORMAT)
        entry["updated_parsed"] = entry["updated"].timetuple()
    
    for entry in feeds["blog"]:
        entry["published"] = datetime.datetime(tzinfo=utc, *entry["published_parsed"][:6]).astimezone(london)
        entry["published_f"] = entry["published"].strftime(DATE_FORMAT)
        entry["published_parsed"] = entry["published"].timetuple()
    
    for entry in feeds["flickr"]:
        entry["published"] = datetime.datetime(tzinfo=utc, *entry["published_parsed"][:6]).astimezone(london)
        entry["published_f"] = entry["published"].strftime(DATE_FORMAT)
        entry["published_parsed"] = entry["published"].timetuple()
        img_re = re.compile(r"""src="(.*?)_m\.jpg""")
        entry["img_src"] = img_re.search(entry["content"][0]["value"]).group(1) + '_s.jpg'
    
    # Munge lifestream feeds
    
    lifestream = feeds["lastfm"] + tweets
    lifestream.sort(lambda x, y: cmp(get_comp_value(x), get_comp_value(y)))
    lifestream.reverse()
    
    # Prep context
    
    context = {
        'body': {
            'id': 'index'
        },
        'lifestream': lifestream,
        'tweets': tweets,
        'feeds': feeds,
    }
    
    template = env.get_template('master.html')
    return Response(template.render(context=context))

urls = (
    (r'^/$', root),
)

application = Application(urls)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 8000, application)
    server.serve_forever()