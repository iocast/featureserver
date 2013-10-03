from vectorformats.exceptions import ExceptionReport


def custom500(error):
    return error.exception.report.encode_exception_report()

error_handlers = {
    500: custom500,
}


class ExceptionWrapper(Exception):
    @property
    def report(self):
        return self._report
    
    def __init__(self, report):
        Exception.__init__(self, "Wrapper for the Exception Report")
        self._report = report

class ExceptionMiddleware(object):
    
    @property
    def app(self):
        return self._app
    @property
    def plugin(self):
        return self._plugin
    
    def __init__(self, app, exception=None, sub_app=True):
        """
            :param app: main application
            :type app: Bottle
            :param exception: exception plugin
            :type exception: ExceptionPlugin
            :param sub_app: wheter to install exception plugin on all sub_applications or not
            :type sub_app: boolean
        """
        
        self._plugin = exception if exception is not None else ExceptionPlugin()
        
        self._app = app
        self.app.install(self._plugin)
        
        if sub_app:
            for route in self.app.routes:
                if route.config.get('mountpoint'):
                    route.config.get('mountpoint').get('target').install(self._plugin)
    

    def __call__(self, environ, start_response):
        self._plugin.clear()
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
    
    def clear(self):
        self.report.clear()

    def postprocessing(self, *args, **kwargs):
        if len(self.report) > 0:
            raise ExceptionWrapper(self.report)

