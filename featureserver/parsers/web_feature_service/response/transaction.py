'''
    Created on Oct 21, 2011
    
    @author: michel
    '''

from action_result import InsertResult, UpdateResult, DeleteResult, ReplaceResult

class TransactionSummary(object):
    
    def __init__(self):
        self._inserts = 0
        self._deletes = 0
        self._updates = 0
        self._replaces = 0
    
    def increase_inserts(self, amount = 1):
        self._inserts += amount
    def increase_deletes(self, amount = 1):
        self._deletes += amount
    def increase_updates(self, amount = 1):
        self._updates += amount
    def increase_replaces(self, amount = 1):
        self._replaces += amount
    
    @property
    def inserts(self):
        return self._inserts
    @property
    def deletes(self):
        return self._deletes
    @property
    def updates(self):
        return self._updates
    @property
    def replaces(self):
        return self._replaces
    

class TransactionResponse(object):
    
    def __init__(self):
        self._summary = None
        self._inserts = []
        self._updates = []
        self._replaces = []
        self._deletes = []
        self._version = '2.0.0'
    
    def add(self, action_result):
        if type(action_result) is InsertResult:
            self.add_insert(action_result)
        elif type(action_result) is UpdateResult:
            self.add_update(action_result)
        elif type(action_result) is DeleteResult:
            self.add_delete(action_result)
        elif type(actionResult) is ReplaceResult:
            self.add_replace(action_result)
    
    @property
    def summary(self):
        return self._summary
    @summary.setter
    def summary(self, summary):
        self._summary = summary

    @property
    def inserts(self):
        return self._inserts
    def add_insert(self, insert):
        self._inserts.append(insert)
        self.summary.increase_inserts()

    @property
    def updates(self):
        return self._updates
    def add_update(self, update):
        self._updates.append(update)
        self.summary.increase_updates()

    @property
    def replaces(self):
        return self._replaces
    def add_replace(self, replace):
        self._replaces.append(replace)
        self.summary.increase_replaces()

    @property
    def deletes(self):
        return self._deletes
    def add_delete(self, delete):
        self._deletes.append(delete)
        self.summary.increase_deletes()
