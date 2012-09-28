#!/usr/bin/python

"""A simple, standalone web server that serves FeatureServer requests."""

__author__  = "MetaCarta"
__version__ = "FeatureServer $Id: featureserver_http_server.py 564 2008-05-24 14:32:18Z crschmidt $"
__license__ = "Clear BSD"
__copyright__ = "2006-2008 MetaCarta"

import mimetypes, os
from optparse import OptionParser
from FeatureServer.Server import wsgi_app_workspace

local_path_location = None

def local_app(environ, start_response):
    if environ['PATH_INFO'].startswith("/static/"):
        global local_path_location
        path = environ['PATH_INFO'].replace("/static/","")
        path.lstrip("/") 
        mime =  mimetypes.guess_type(path)
        try:
            f = open(os.path.join(local_path_location, path))
            start_response("200 OK", [("Content-Type",mime[0])])
            return [f.read()]
        except Exception, E:
            start_response("404 Not Found", [("Content-Type","text/plain")])
            return ["Not found: %s" % E]
            
    return wsgi_app_workspace(environ, start_response)

def run(port=8081, thread=False, local_path=""):
    from wsgiref import simple_server
    if thread:
        from SocketServer import ThreadingMixIn
        class myServer(ThreadingMixIn, simple_server.WSGIServer):
            pass 
    else:
        class myServer(simple_server.WSGIServer):
            pass

    httpd = myServer(('',port), simple_server.WSGIRequestHandler,)
    if local_path:
        global local_path_location
        local_path_location = local_path
        httpd.set_app(local_app)
    else:
        httpd.set_app(wsgi_app_workspace)
    
    try:
        print "Listening on port %s" % port
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down."

if __name__ == '__main__':
    parser = OptionParser(version=__version__, description=__doc__)
    parser.add_option("-p", "--port", 
        help="port to run webserver on. Default is 8080", 
        dest="port", 
        action='store', 
        type="int", 
        default=8080)
    parser.add_option("-t", help="enable threading in HTTP Server.", dest="thread", action="store_true", default=False)   
    parser.add_option("-l", help="serve files from local disk", dest="local_path")

    (options, args) = parser.parse_args()
    run(options.port, options.thread, options.local_path)


