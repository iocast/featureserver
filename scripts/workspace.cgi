#!/usr/bin/python

#CGI
if __name__ == '__main__':
    from FeatureServer.Server import Server, cfgfiles, cgi
    service = Server.load(*cfgfiles)
    cgi(service.dispatchWorkspaceRequest)


#WSGI
else:
    # to enable, add to .htaccess:  
    #     AddHandler wsgi-script .cgi

    # wsgi is more picky about the paths.
    import sys, os
    path = os.path.dirname(__file__)
    sys.path.append(path)

    from FeatureServer.Server import Server, wsgi, cfgfiles
    # make all the paths absolute as well.
    cfgfiles = list(cfgfiles) + [os.path.join(path, f) for f in cfgfiles if not f.startswith('/')]

    service = Server.load(*cfgfiles)
    def application(environ, start_response):
        return wsgi(service.dispatchWorkspaceRequest, environ, start_response)

