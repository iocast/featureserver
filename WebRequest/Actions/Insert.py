'''
Created on November 12, 2012
    
@author: michel
'''

from Action import Action


class Insert(Action):
    
    def __init__(self, datasource, **kwargs):
        super(Insert, self).__init__("insert", datasource, **kwargs)
        
    