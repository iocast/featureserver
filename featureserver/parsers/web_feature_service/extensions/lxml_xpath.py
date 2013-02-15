

class DataSourceExtension(object):
    @property
    def datasource(self):
        return self._datasource
    
    def __init__(self, datasource, *args, **kwargs):
        super(DataSourceExtension, self).__init__(*args, **kwargs)
        self._datasource = datasource



class PostGISHstoreExtension(DataSourceExtension):
    '''
        usage:
        >>> from lxml import etree
        >>> from featureserver.parsersextensions import lxml_xpath as ext_lxml
        
        >>> xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/tst.xsl")
        
        >>> ext_module = ext_lxml.PostGISHstoreExtension(self.datasource)
        >>> functions = ('hstore_attribute', 'is_hstore', 'clip_hstore')
        >>> extensions = etree.Extension( ext_module, functions, ns='http://featureserver.org' )
        
        >>> transform = etree.XSLT(xslt, extensions=extensions)
        
        >>> result = transform(etree.fromstring(xml_string))
        
        in the XSL file you can use it as follow:
        >>> <xsl:stylesheet version="2.0" xmlns:fs="http://featureserver.org" ...>
        >>> <xsl:value-of select="fs:hstore_atribute()" />
        >>> <xsl:if test="fs:is_hstore(.)">...</xsl:if>
    '''
    
    def __init__(self, datasource, *args, **kwargs):
        super(PostGISHstoreExtension, self).__init__(datasource, *args, **kwargs)

    def hstore_attribute(self, _):
        return str(self.datasource.hstore_attribute)

    def is_hstore(self, _, args):
        if self.datasource.hstore_attribute in args:
            return True
        return False

    def clip_hstore(self, _, args):
        return str(args[0])[str(args[0]).index('||')+4:-1]


