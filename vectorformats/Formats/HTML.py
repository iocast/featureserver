from vectorformats.Feature import Feature
from vectorformats.Formats.Format import Format

from Cheetah.Template import Template

class HTML (Format):
    """Uses Cheetah to format a list of features."""

    template_file = "template/default.html"
    """Default template file to use."""

    def encode(self, result, **kwargs):
        template = self.template()
        output = Template(template, searchList = [{'features':result}, self])
        return str(output)
    
    def template(self):
        return file(self.template_file).read()
