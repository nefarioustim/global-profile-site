# -*- coding: utf-8 -*-

import os, sys
APP_BASE        = os.path.join( os.path.dirname( __file__ ), '..' )
LIB_BASE        = os.path.join( APP_BASE, 'lib' )
TEMPLATES_BASE  = os.path.join( APP_BASE, 'templates' )

sys.path.insert( 0, LIB_BASE )

from newf import Application, Response, ResponseRedirect
from jinja2 import Environment, FileSystemLoader

env = Environment( loader = FileSystemLoader( TEMPLATES_BASE ) )

def root(request):
    context = {
        'body' : {
            'id' : 'index'
        },
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