#!/usr/bin/python
from featureserver.server import wsgi_app

import sys

if __name__ == '__main__':
    from flup.server.fcgi_fork  import WSGIServer
    WSGIServer(wsgi_app).run()
