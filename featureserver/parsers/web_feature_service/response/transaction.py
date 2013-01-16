'''
    Created on Oct 21, 2011
    
    @author: michel
    '''

from action_result import InsertResult, UpdateResult, DeleteResult, ReplaceResult

class TransactionSummary(object):
    
    def __init__(self):
        self.totalInserted = 0
        self.totalDeleted = 0
        self.totalUpdated = 0
        self.totalReplaced = 0
    
    def increaseInserted(self, amount = 1):
        self.totalInserted += amount
    def increaseDeleted(self, amount = 1):
        self.totalDeleted += amount
    def increaseUpdated(self, amount = 1):
        self.totalUpdated += amount
    def increaseReplaced(self, amount = 1):
        self.totalReplaced += amount
    
    def getTotalInserted(self):
        return self.totalInserted
    def getTotalDeleted(self):
        return self.totalDeleted
    def getTotalUpdated(self):
        return self.totalUpdated
    def getTotalReplaced(self):
        return self.totalReplaced


class TransactionResponse(object):
    
    def __init__(self):
        self.summary = None
        self.insertResults = []
        self.updateResults = []
        self.replaceResults = []
        self.deleteResults = []
        self.version = '2.0.0'
    
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


