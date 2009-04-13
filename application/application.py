# -*- coding: utf-8 -*-

import os, sys
APP_BASE        = os.path.join( os.path.dirname( __file__ ), '..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )
TEMPLATES_BASE  = os.path.join( APP_BASE, 'templates' )

sys.path.insert( 0, LIB_BASE )

import pickle
from newf import Application, Response, ResponseRedirect
from jinja2 import Environment, FileSystemLoader

env = Environment( loader = FileSystemLoader( TEMPLATES_BASE ) )

def root(request):
	import datetime
	import re
	cache = open( os.path.join( APP_BASE, 'var/cache/twitter.pkl' ), 'rb')
	tweets, last_modified = pickle.load(cache)
	cache.close()
	
	for tweet in tweets:
		tweet[ "text" ] = re.sub( r'http://([\w.\-/?#&;]+)', r"""<a href="http://\1">http://\1</a>""", tweet["text"] )
		tweet[ "text" ] = re.sub( r'@(\w+)', r"""<a href="http://twitter.com/\1/">@\1</a>""", tweet["text"] )
		tweet[ "created_at_f" ] = tweet[ "created_at" ].strftime( "%d %b at %H:%M" )
	
	context = {
        'body' : {
            'id' : 'index'
        },
		'tweets' : tweets
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