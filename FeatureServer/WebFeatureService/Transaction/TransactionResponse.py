'''
Created on Oct 21, 2011

@author: michel
'''
from FeatureServer.WebFeatureService.Transaction.TransactionSummary import TransactionSummary

class TransactionResponse(object):
    
    summary = None
    insertResults = []
    updateResults = []
    replaceResults = []
    version = '2.0.0'
    
    def setSummary(self, summary):
        self.summary = summary
    
    def getSummary(self):
        return self.summary
    
    def addInsertResult(self, insertResult):
        self.insertResults.append(insertResult)
    
    def getInsertResults(self):
        return self.insertResults

    def addUpdateResult(self, updateResult):
        self.updateResults.append(updateResult)
    
    def getUpdateResults(self):
        return self.updateResults

    def addReplaceResult(self, replaceResult):
        self.replaceResults.append(replaceResult)
    
    def getReplaceResults(self):
        return self.replaceResults
        