'''
Created on Oct 21, 2011

@author: michel
'''
from TransactionSummary import TransactionSummary

from InsertResult import InsertResult
from UpdateResult import UpdateResult
from DeleteResult import DeleteResult
from ReplaceResult import ReplaceResult

class TransactionResponse(object):
    
    summary = None
    insertResults = []
    updateResults = []
    replaceResults = []
    deleteResults = []
    version = '2.0.0'
    
    def setSummary(self, summary):
        self.summary = summary
    
    def getSummary(self):
        return self.summary
    
    def addResult(self, actionResult):
        if type(actionResult) is InsertResult:
            self.addInsertResult(actionResult)
        elif type(actionResult) is UpdateResult:
            self.addUpdateResult(actionResult)
        elif type(actionResult) is DeleteResult:
            self.addDeleteResult(actionResult)
        elif type(actionResult) is ReplaceResult:
            self.addReplaceResult(actionResult)
        
    
    def addInsertResult(self, insertResult):
        self.insertResults.append(insertResult)
        self.getSummary().increaseInserted()
    
    def getInsertResults(self):
        return self.insertResults
    

    def addUpdateResult(self, updateResult):
        self.updateResults.append(updateResult)
        self.getSummary().increaseUpdated()
    
    def getUpdateResults(self):
        return self.updateResults
    

    def addReplaceResult(self, replaceResult):
        self.replaceResults.append(replaceResult)
        self.getSummary().increaseReplaced()
    
    def getReplaceResults(self):
        return self.replaceResults
    
    
    def addDeleteResult(self, deleteResult):
        self.deleteResults.append(deleteResult)
        self.getSummary().increaseDeleted()
    
    def getDeleteResults(self):
        return self.deleteResults

