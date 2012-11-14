'''
Created on November 12, 2012
    
@author: michel
'''

from Action import Action


class Select(Action):
    
    def __init__(self, datasource, **kwargs):
        super(Select, self).__init__("select", datasource, **kwargs)
