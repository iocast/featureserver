from featureserver.exceptions import ExceptionReport



def custom500(error):
    return "your fucked"

error_handlers = {
    500: custom500,
}


class ExceptionMiddleware(object):
    @property
    def app(self):
        return self._app
    
    def __init__(self, app, exception, sub_app=True):
        self._app = app
        self.app.install(exception)
        
        if sub_app:
            for route in self.app.routes:
                if route.config.get('mountpoint'):
                    route.config.get('mountpoint').get('target').install(exception)
    

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


class ExceptionPlugin(object):
    name = 'exception-report'
    api = 2
    
    
    @property
    def report(self):
        return self._report
    @report.setter
    def report(self, report):
        self._report = report

    def __init__(self):
        self.report = ExceptionReport
        self._apps = []
    
    def setup(self, app):
        self._apps.append(app)

    def apply(self, callback, route):
        return callback

