import bottle
from ..errors import error_handlers
from featureserver.exceptions import ServiceException

app = bottle.Bottle()
app.error_handler = error_handlers

@app.route('/')
@app.route('/services.<format>')
@app.route('/index.<format>')
def wfs_list(format=None):
    if format is not None:
        if format not in app.config.app.services:
            app.config.app.errors.add(ServiceException("main", format))
    return "use one of the following service <strong>%s</strong>" % (" ,".join(app.config.app.services))



@app.hook('after_request')
def after():
    if len(app.config.app.errors) > 0:
        raise ServiceException("main", "asdf")
    return "<strong>you're fucked</strong>"

