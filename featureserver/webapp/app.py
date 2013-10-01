from ConfigParser import ConfigParser
from featureserver.exceptions import ExceptionReport


class Application(object):
    
    @property
    def config(self):
        return self._config
    
    @property
    def services(self):
        return self._config["featureserver"]["services"]
    
    @property
    def errors(self):
        return self._errors
    
    def __init__(self, config=None):
        super(Application, self).__init__()
        self._config = config
        self._errors = ExceptionReport()



def get(config=None):
    from .services import main
    
    application = Application(config)
    
    main.app.config.id = "featureserver"
    main.app.config.prefix = ""
    main.app.config.path= ""
    main.app.config.app = application
    
    
    from .services import rest
    rest.app.config.id = lambda: main.app.config.id + ".rest"
    rest.app.config.prefix = "/rest"
    rest.app.config.path = lambda: main.app.config.path + rest.app.config.prefix
    rest.app.config.app = application
    main.app.mount(app=rest.app, prefix=rest.app.config.prefix)
    
    
    from .services import wfs
    wfs.app.config.id = lambda: main.app.config.id + ".wfs"
    wfs.app.config.prefix = "/wfs"
    wfs.app.config.path = lambda: main.app.config.path + wfs.app.config.prefix
    wfs.app.config.app = application
    main.app.mount(app=wfs.app, prefix=wfs.app.config.prefix)
    
    
    return main.app

