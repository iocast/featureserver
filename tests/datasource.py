from featureserver.parsers.web_feature_service.response.transaction import TransactionResponse, TransactionSummary

class Base(object):
    def __init__ (self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    
    @property
    def fs(self):
        return self._fs

    def ds_dispatch(self, ds_id, request):
        request.parse(self.fs)
        
        transactions = TransactionResponse()
        transactions.summary = TransactionSummary()
        
        self.fs.datasources['fs_point'].begin()
        for action in request.service.datasources[ds_id]:
            method = getattr(self.fs.datasources[ds_id], action.method)
            result = method(action)
            transactions.add(result)

        return transactions

