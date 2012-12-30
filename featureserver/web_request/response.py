from StringIO import StringIO

class Response(object): 

    def __init__(self, data="", content_type="text/plain", headers = None, status_code="200 OK", encoding='utf-8'):
        self.data = data
        self.content_type = content_type
        self.extra_headers = headers
        self.status_code = status_code
        self.encoding = encoding
    
    def getData(self):
        if isinstance(self.data, StringIO):
            return self.data.getvalue()
        if len(self.encoding) > 0:
            return self.data.encode(self.encoding)
        else:
            return str(self.data)