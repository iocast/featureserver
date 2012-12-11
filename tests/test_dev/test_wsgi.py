import twill
import twill.commands as tc
from cStringIO import StringIO
#import wsgi_intercept.mechanize_intercept


host = 'localhost'
port = 8081

full_host = '%s:%i' % (host, port)
def setup():
    def create_app():
        import sys, os
        path = os.path.dirname(__file__)
        sys.path.append(path)
        sys.path.insert(0, os.path.abspath("."))
        # add the path to simplify
        sys.path.append(os.path.join(os.path.abspath("."), 'doc/examples'))
        import Simplify

        from FeatureServer.Server import Server, wsgi, cfgfiles
        # make all the paths absolute as well.
        cfgfiles = list(cfgfiles) + [os.path.join(path, f) for f in cfgfiles if not f.startswith('/')]

        service = Server.load(*cfgfiles)

        def app(environ, start_response):
            return wsgi(service.dispatchRequest, environ, start_response)

        return app


    twill.add_wsgi_intercept(host, port, create_app)
    # argh. cant POST with twill...
    # argh wsgi_intercept is broken...
    #wsgi_intercept.add_wsgi_intercept(host, port, create_app)


def teardown():
    pass


def test_connect():
    tc.go('http://%s/' % full_host)
    # this will unless scribble is in the output
    tc.find('scribble')
    
# wsgi-intercept is broken. cant POST
#def test_post():
#    b = wsgi_intercept.mechanize_intercept.Browser()
#    b.open('http://%s/' % full_host)
#    # response.read()


def test_services():
    tc.go('http://%s/scribble/1.geojson' % full_host)
    tc.find('{')

    tc.go('http://%s/scribble/1.wfs' % full_host)
    tc.find('wfs')

    # this may fail because wsgi requires the full
    # path to the template... fix?
    tc.go('http://%s/scribble/1.html' % full_host)
    tc.find('openlayers')

    tc.go('http://%s/scribble/1.georss' % full_host)
    tc.find('<feed')

    tc.go('http://%s/scribble/1.osm' % full_host)
    tc.find('<osm')
    

# this test wont work with relative paths in the .cfg
def test_processing_simplify():
    """cfg:

    [process_simplify]
    module=Simplify
    class=Simplify
    tolerance_default=.1
    tolerance_locked=no

    [scribble]
    type=SQLite
    file=/var/www/ms_tmp/featureserver.scribble
    gaping_security_hole=yes
    template=template/default-withmap.html
    processes=simplify
    """

    s1 = StringIO()
    twill.set_output(s1)
    tc.go('http://%s/scribble/1.geojson?process_simplify_tolerance=0.001' % full_host)
    tc.show()

    s2 = StringIO()
    twill.set_output(s2)
    tc.go('http://%s/scribble/1.geojson?process_simplify_tolerance=100' % full_host)
    tc.show()
    s1 = s1.getvalue()
    s2 = s2.getvalue()
    #import sys 
    #print >>sys.stderr, s1
    #print >>sys.stderr, ''
    #print >>sys.stderr, s2

    assert 'processed_by' in s2
    
    # it's simplified so it should be shorter ... add a better test...
    assert len(s2) <= len(s1)


