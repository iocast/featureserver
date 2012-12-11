'''
Created on November 12, 2012
    
@author: michel
'''

from Action import Action


class Update(Action):
    
    def __init__(self, datasource, **kwargs):
        super(Update, self).__init__("update", datasource, **kwargs)
