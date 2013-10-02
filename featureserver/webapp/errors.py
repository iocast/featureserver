from vectorformats.exceptions import ExceptionReport


def custom500(error):
    return str(error.exception.report.encode_exception_report())
    
#return "your fucked 500 " + str(len(error.exception.report))

error_handlers = {
    500: custom500,
}


class ExceptionWrapper(Exception):
    @property
    def report(self):
        return self._report
    
    def __init__(self, report):
        print report.encode_exception_report()
        Exception.__init__(self, "Wrapper for the Exception Report")
        self._report = report

class ExceptionMiddleware(object):
    
    @property
    def app(self):
        return self._app
    
    def __init__(self, app, exception=None, sub_app=True):
        """
            :param app: main application
            :type app: Bottle
            :param exception: exception plugin
            :type exception: ExceptionPlugin
            :param sub_app: wheter to install exception plugin on all sub_applications or not
            :type sub_app: boolean
        """
        
        if exception is None:
            exception = ExceptionPlugin()
        
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
        self.report = ExceptionReport()
        self._apps = []
    
    def setup(self, app):
        self._apps.append(app)
        for app in self._apps:
            app.add_error = self.add
            app.error_handler = error_handlers
            app.hooks.add('after_request', self.postprocessing)


    def apply(self, callback, route):
        return callback

    def add(self, error):
        self.report.add(error)

    def postprocessing(self, *args, **kwargs):
        if len(self.report) > 0:
            raise ExceptionWrapper(self.report)

