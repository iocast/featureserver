'''
Created on Nov 29, 2012
    
@author: michel
'''

import os
from lxml import etree

class FilterResources(object):
    
    node = None
    
    def __init__(self, node):
        self.node = node
    
    def render(self, service):
        xslt = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/../../../../resources/filterencoding/filter_resources.xsl")
        transform = etree.XSLT(xslt)
        result = transform(self.node, version = "'" + str(service.version) + "'")
        
        elements = result.xpath("//Resources")
        if len(elements) > 0:
            str_list =  elements[0].text.strip().split(',')
            str_list = filter(None, str_list)
            str_list = filter(lambda x: len(x) > 0, str_list)
            return str_list
        return []

