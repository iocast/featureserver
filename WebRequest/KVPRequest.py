'''
'''

from WebRequest.Request import Request

class KVPRequest(Request):

    def find_request(self):
        # check GET params
        if not self.params.has_key('request'):
            self.params['request'] = "GetCapabilities"
    
    
    def find_service(self):
        # check POST data
        if len(self.post_kvp) > 0:
            for key, value in self.post_kvp:
                if key.lower() == 'service':
                    if value.lower() in self.content_types:
                        self.service = self.content_types[value.lower()]
                        return

        # check GET data
        if self.params.has_key('service'):
            if self.params['service'].lower() in self.content_types:
                self.service = self.content_types[self.params['service'].lower()]
                return
                    
        # check file extension in URL
        if len(self.path) > 1:
            path_pieces = self.path[-1].split(".")
            if len(path_pieces) > 1:
                if path_pieces[-1].lower() in self.content_types:
                    self.service = self.content_types[path_pieces[-1].lower()]
                    return

        super(KVPRequest, self).find_service()


    def find_typenames(self):
        # check POST data
        if len(self.post_kvp) > 0:
            for key, value in self.post_kvp:
                if key.lower() == 'typename':
                    self.datasources.update({key : [] for key in value.split(",")})
                    return
        # check GET data
        if self.params.has_key('typename'):
            self.datasources.update({key : [] for key in self.params['typename'].split(",")})
            return

    def find_version(self):
        # check POST data
        if len(self.post_kvp) > 0:
            for key, value in self.post_kvp:
                if key.lower() == 'version':
                    self.version = str(value)
                    return
    
        # check GET data
        if self.params.has_key('version'):
            self.version = str(self.params['version'])
            return


