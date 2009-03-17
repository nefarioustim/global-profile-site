# -*- coding: utf-8 -*-

import os, sys
APP_BASE        = os.path.join( os.path.dirname( __file__ ), '..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )
TEMPLATES_BASE  = os.path.join( APP_BASE, 'templates' )

sys.path.insert( 0, LIB_BASE )

from newf import Application, Response, ResponseRedirect
from jinja2 import Environment, FileSystemLoader
import twitter, twitter.sensitive

env = Environment( loader = FileSystemLoader( TEMPLATES_BASE ) )

def root(request):
    # Dies here for some reason. Must be something to do with the HTTP
    # connection since the __init__ validates the login credentials. No log
    # message though; access or error.
    twitapi = twitter.Twitter( twitter.sensitive.twitter_user, twitter.sensitive.twitter_passwd )
    
    context = {
        'body' : {
            'id' : 'index'
        },
        'twitter' : twitapi.get_friends_timeline()
    }
    
    template = env.get_template('master.html')
    return Response(template.render(context))

urls = (
	(r'^/$', root),
)

application = Application(urls)

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	server = make_server('', 8000, application)
	server.serve_forever()