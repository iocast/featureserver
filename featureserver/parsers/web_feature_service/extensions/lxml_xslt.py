'''
'''
import os
from lxml import etree

class DataSourceExtension(etree.XSLTExtension):
    '''
        >>> <xsl:stylesheet version="1.0" xmlns:fs="http://featureserver.org" extension-element-prefixes="fs">
    
        >>> <xsl:template match="*">
        >>>     <fs:python-extension>
        >>>         <some-content />
        >>>     </fs:python-extension>
        >>> </xsl:template>
    '''
    @property
    def datasource(self):
        return self._datasource
    
    def __init__(self, datasource, *args, **kwargs):
        super(DataSourceExtension, self).__init__(*args, **kwargs)
        self._datasource = datasource


class ForEachGroupExtension(DataSourceExtension):

    def __init__(self, datasource, *args, **kwargs):
        super(ForEachGroupExtension, self).__init__(datasource, *args, **kwargs)


