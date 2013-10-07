from ConfigParser import ConfigParser
from .errors import ExceptionMiddleware


class Application(object):
    
    @property
    def config(self):
        return self._config
    
    @property
    def services(self):
        return self._config["server"]["services"]
    
    @property
    def default_format(self):
        return self._config["server"]["defaults"]["format"]
    
    def __init__(self, config=None):
        super(Application, self).__init__()
        self._config = config



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
    
    
    
    return ExceptionMiddleware(main.app)

