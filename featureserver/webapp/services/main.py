import bottle
from featureserver.exceptions import ServiceException

app = bottle.Bottle()

@app.route('/')
@app.route('/services.<format>')
@app.route('/index.<format>')
def wfs_list(format=None):
    if format is not None:
        if format not in app.config.app.services:
            app.add_error(ServiceException("main", format))
    return "use one of the following service <strong>%s</strong>" % (" ,".join(app.config.app.services))


