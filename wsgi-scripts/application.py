# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

from newf import Application, Response, ResponseRedirect
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('/Users/Shared/Sites/timhuegdon.com/templates'))

def root(request):
    template = env.get_template('master.html')
    return Response(template.render({'body_id': 'index'}))

urls = (
	(r'^/$', root),
)

application = Application(urls)

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	server = make_server('', 8000, application)
	server.serve_forever()