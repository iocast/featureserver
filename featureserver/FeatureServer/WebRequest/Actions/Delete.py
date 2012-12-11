'''
Created on November 12, 2012
    
@author: michel
'''

from Action import Action


class Delete(Action):
    
    def __init__(self, datasource, **kwargs):
        super(Delete, self).__init__("delete", datasource, **kwargs)
