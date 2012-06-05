__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: HTML.py 561 2008-05-23 12:01:15Z crschmidt $"

from __init__ import Request
from Cheetah.Template import Template

class HTML (Request):
    default_template = "template/default.html"
    metadata_template = "templates/layers.html"

    def _datasource (self):
        return self.service.datasources[self.datasources[0]]
    
    def encode_metadata(self, action):
        layers = self.service.datasources
        if self.service.metadata.has_key("metadata_template"):
            self.metadata_template = self.service.metadata['metadata_template']
            
        template = file(self.metadata_template).read()
        output = Template(template, searchList = [{'layers': layers, 'datasource':self.datasources[0]}, self])
        return  "text/html; charset=utf-8", str(output).decode("utf-8")

    def encode(self, result):
        template = self.template()
        output = Template(template, searchList = [{'actions':result, 'datasource':self.datasources[0]}, self])
        return ("text/html; charset=utf-8", str(output).decode("utf-8"), None, 'utf-8')
    
    def template(self, name="default_template"):
        datasource = self._datasource()
        if hasattr(datasource, "default_template"):
            template = datasource.default_template
        else:
            template = self.default_template
        return file(template).read()
