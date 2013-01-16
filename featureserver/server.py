#!/usr/bin/python
__author__  = "MetaCarta"
__copyright__ = "Copyright (c) 2006-2008 MetaCarta"
__license__ = "Clear BSD" 
__version__ = "$Id: Server.py 607 2009-04-27 15:53:15Z crschmidt $"

import sys
import time
import os
import traceback
import ConfigParser
from .web_request.handlers import wsgi, mod_python, cgi
from .web_request.request import Request
from lxml import etree
import cgi as cgimod

from .parsers.web_feature_service.response.transaction import TransactionResponse, TransactionSummary
from .parsers.web_feature_service.response.action_result import ActionResult

from .workspace.filesystem import FileHandler

from .exceptions.core import BaseException, ExceptionReport
from .exceptions.wfs import InvalidValueException
from .exceptions.datasource import ConnectionException
from .exceptions.configuration import LayerNotFoundException


import processing
from .web_request.response import Response

# First, check explicit FS_CONFIG env var
if 'FS_CONFIG' in os.environ:
    cfgfiles = os.environ['FS_CONFIG'].split(",")
# Otherwise, make some guesses.
else:
    # Windows doesn't always do the 'working directory' check correctly.
    workingdir = os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))
    realpath = os.path.dirname(os.path.abspath(__file__))
    if sys.platform == 'win32':
        cfgfiles = (os.path.join(workingdir, "config", "featureserver.cfg"), os.path.join(workingdir, ".." , "config" , "featureserver.cfg"), os.path.join(realpath, "config", "featureserver.cfg"), os.path.join(realpath, "..", "config", "featureserver.cfg"))
    else:
        cfgfiles = ("featureserver.cfg", os.path.join("..", "config", "featureserver.cfg"), "/etc/featureserver.cfg", os.path.join(realpath, "config", "featureserver.cfg"), os.path.join(realpath, "..", "config", "featureserver.cfg"))

class Server (object):
    """The server manages the datasource list, and does the management of
       request input/output.  Handlers convert their specific internal
       representation to the parameters that dispatchRequest is expecting,
       then pass off to dispatchRequest. dispatchRequest turns the input 
       parameters into a (content-type, response string) tuple, which the
       servers can then return to clients. It is possible to integrate 
       FeatureServer into another content-serving framework like Django by
       simply creating your own datasources (passed to the init function) 
       and calling the dispatchRequest method. The Server provides a classmethod
       to load datasources from a config file, which is the typical lightweight
       configuration method, but does use some amount of time at script startup.
       """ 
       
    def __init__ (self, datasources, metadata = {}, processes = {}):
        self.datasources   = datasources
        self.metadata      = metadata
        self.processes     = processes
    
    @property
    def datasources(self):
        return self._datasources
    @datasources.setter
    def datasources(self, datasources):
        self._datasources = datasources
    
    @property
    def metadata(self):
        return self._metadata
    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata
    @property
    def metadata_output(self):
        if 'default_output' in self._metadata:
            return self._metadata['default_output']
    @property
    def metadata_exception(self):
        if 'default_exception' in self._metadata:
            return self._metadata['default_exception']
    @property
    def log(self):
        if 'error_log' in self._metadata:
            return self._metadata['error_log']

    @property
    def processes(self):
        return self._processes
    @processes.setter
    def processes(self, processes):
        self._processes = processes

    
    
    def _loadFromSection (cls, config, section, module_type, **objargs):
        type  = config.get(section, "type")
        module = __import__("%s.%s" % (module_type, type), globals(), locals(), type)
        objclass = getattr(module, type)
        for opt in config.options(section):
            objargs[opt] = config.get(section, opt)
        if module_type is 'datasource':
            return objclass(section, **objargs)
        else:
            return objclass(**objargs)
    loadFromSection = classmethod(_loadFromSection)

    def _load (cls, *files):
        """Class method on Service class to load datasources
           and metadata from a configuration file."""
        config = ConfigParser.ConfigParser()
        config.read(files)
        
        metadata = {}
        if config.has_section("metadata"):
            for key in config.options("metadata"):
                metadata[key] = config.get("metadata", key)

        processes = {}
        datasources = {}
        for section in config.sections():
            if section == "metadata": continue
            if section.startswith("process_"):
                try:
                    processes[section[8:]] = FeatureServer.Processing.loadFromSection(config, section)
                except Exception, E:
                    pass 
            else:     
                datasources[section] = cls.loadFromSection(config, section, 'datasource')

        return cls(datasources, metadata, processes)
    load = classmethod(_load)


    def dispatchRequest (self, request):
        """Read in request data, and return a (content-type, response string) tuple. May
           raise an exception, which should be returned as a 500 error to the user."""
        exceptions = ExceptionReport()
        service = None
        
        try:
            # parse request and extend exception report
            exceptions.extend(request.parse(self))
        except Exception as e:
            # TODO: handle fatal error correctly
            # fatal error occured during parsing request
            if "code" not in e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exceptions.add(BaseException(**{'message':str(e), 'code':"", 'locator':"", 'layer':"", 'dump':repr(traceback.format_exception(exc_type, exc_value, exc_traceback))}))
            else:
                exceptions.add(e)
            return self.respond_report(report=exceptions, service=service)
        
        if exceptions.has_exceptions():
            return self.respond_report(report=exceptions, service=request.service, status_code="400 Bad request")
    
        # list of class Feature
        response = []
        
        # handle special action on the output format such as:
        #   - GetCapabilities or DescribeFeatureType
        for action in request.service.actions:
            # if datasource is empty, try to find the method on the service object
            mime, data, headers, encoding = getattr(request.service.output, action.method.lower())()
            return self.respond(mime = mime, data = data, headers = headers, encoding = encoding)                


        
        transactions = TransactionResponse()
        transactions.setSummary(TransactionSummary())
        
        try:
            # handle normal actions on the datasource
            for (typename, actions) in request.service.datasources.iteritems():
                datasource = self.datasources[typename]
                
                datasource.begin()
                
                for action in actions:
                    method = getattr(datasource, action.method)

                    result = method(action)
                    
                    if isinstance(result, ActionResult):
                        transactions.addResult(result)
                    elif result is not None:
                        response += result
            
            # TODO: only commit if connection is open
            # commit all changes
            for typename in request.service.datasources.keys():
                self.datasources[typename].commit()
        except Exception as e:
            # TODO: only rollback if connection is open
            # call rollback on every requested datasource
            for typename in request.service.datasources.keys():
                self.datasources[typename].rollback()
            if "code" not in e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exceptions.add(BaseException(**{'message':str(e), 'code':"", 'locator':"", 'layer':"", 'dump':repr(traceback.format_exception(exc_type, exc_value, exc_traceback))}))
            else:
                exceptions.add(e)

        if exceptions.has_exceptions():
            return self.respond_report(report=exceptions, service=request.service)

        if transactions.summary.totalDeleted > 0 or transactions.summary.totalInserted > 0 or transactions.summary.totalUpdated > 0 or transactions.summary.totalReplaced > 0:
            response = transactions

        return self.respond_service(response=response, service=request.service)
    
    
    # TODO: should it be service -> default_exception -> default_output -> WFS
    #                    default_exception -> servcie -> default_output -> WFS
    def respond_report(self, report, service, status_code="500 Internal Error"):
        try:
            output_module = __import__("output_format.%s" % self.metadata_exception, globals(), locals(), self.metadata_exception)
            output = getattr(output_module, self.metadata_exception)
            default_exception = output(self)
                
            if hasattr(default_exception, "default_exception"):
                mime, data, headers, encoding = default_exception.encode_exception_report(report)
                return self.respond(mime=mime, data=data, headers=headers, encoding=encoding, status_code=status_code)
            else:
                raise Exception("Defined service of key 'default_exception' does not support encoding exception reports. Please use a supported service or disable this key.")
        except:
            # check if service supports exception encoding
            if service is not None and service.output is not None and hasattr(service.output, "encode_exception_report"):
                mime, data, headers, encoding = service.output.encode_exception_report(report)
                return self.respond(mime=mime, data=data, headers=headers, encoding=encoding, status_code=status_code)
            else:
                try:
                    # get default service and instantiate
                    output_module = __import__("output_format.%s" % self.metadata_output, globals(), locals(), self.metadata_output)
                    output = getattr(output_module, self.metadata_output)
                    default_output = output(self)
                
                    if hasattr(default_output, "encode_exception_report"):
                        mime, data, headers, encoding = default_output.encode_exception_report(report)
                        return self.respond(mime=mime, data=data, headers=headers, encoding=encoding, status_code=status_code)
                    else:
                        # load WFS for exception handling
                        from .output_format.wfs import WFS
                        wfs_output = WFS(self)
                        mime, data, headers, encoding = wfs_output.encode_exception_report(report)
                        return self.respond(mime=mime, data=data, headers=headers, encoding=encoding, status_code=status_code)
                except: raise
                    #raise Exception("Required key 'default_output' in the configuration file is not set. Please define a default output.")


    def respond_service(self, response, service):
        mime, data, headers, encoding = service.output.encode(response)
        return self.respond(mime = mime, data = data, headers = headers, encoding = encoding)

    def respond(self, mime, data, headers, encoding, status_code="200 OK"):
        return Response(data=data, content_type=mime, headers=headers, status_code=status_code, encoding=encoding)
        





    def dispatchWorkspaceRequest (self, request):
        handler = FileHandler('workspace.db')
        handler.removeExpired()
        
        # create workspace
        if params.has_key("base"):
            if params.has_key("request"):
                
                identifier = ''
                if params.has_key('id'):
                    identifier = params['id']
                    
                short = handler.create(params['base'], params['request'], identifier)
                
                output = ""
                 
                if params.has_key("callback"):
                    output += params["callback"] + '('
                
                output += '{"key":"' + short + '"}'
                
                if params.has_key("callback"):
                    output += ');'
                     
                return Response(data=output.decode("utf-8"), content_type="application/json; charset=utf-8", status_code="200 OK")
            
        
        # handle WFS request
        elif params.has_key('key'):
            
            handler.updateLastAccess(params['key'])
            data = handler.getByKey(params['key'])
            if len(data) > 0:                    
                #generate workspace specific datasource
                for layer in self.datasources:
                    if layer == data[2]:
                        self.datasources = {layer : self.datasources[layer]}
                        self.datasources[layer].abstract += " :: " + str(data[0])
                        break
                        
                if params.has_key('request'):
                    if params['request'].lower() == 'getfeature':
                        if params.has_key('filter') <> True:
                            if post_data == None:
                                params['filter'] = data[3]
                    
                    return self.dispatchRequest(Request(base_path=base_path, path_info=path_info, params=params, request_method=request_method, post_data=post_data, acccepts=accepts))
        
        # check workspace by id
        elif params.has_key('skey'):
            output = ""
            if params.has_key("callback"):
                output += params["callback"] + '('
            output += '{"workspaces":['
            
            data = handler.getByKey(params['skey'])
            if len(data) > 0:
                date = time.strftime("%a %b %d, %Y  %I:%M:%S %p",time.localtime(float(data[4])))
                output += '{"Workspace":"'+data[0]+'","LastAccess":"' + date  + '"},'
                             
            output += "]}"
            if params.has_key("callback"):
                output += ');'
            
            return Response(data=output.decode("utf-8"), content_type="application/json; charset=utf-8", status_code="200 OK")
        
        # check workspace by email
        elif params.has_key('sid'):
            output = ""
            if params.has_key("callback"):
                output += params["callback"] + '('
            output += '{"workspaces":['
            
            workspaces = handler.getByIdentifier(params['sid'])
            
            for data in workspaces:
            
                date = time.strftime("%a %b %d, %Y  %I:%M:%S %p",time.localtime(float(data[4])))
                output += '{"Workspace":"'+data[0]+'","LastAccess":"' + date  + '"},'
            
            if len(data) > 0:
                output = output[:-1] 
            
            output += "]}"
            if params.has_key("callback"):
                output += ');'
            
            return Response(data=output.decode("utf-8"), content_type="application/json; charset=utf-8", status_code="200 OK")
        
        #TODO: not available
        return None

theServer = None
lastRead = 0

#def handler (apacheReq):
#    global theServer
#    if not theServer:
#        options = apacheReq.get_options()
#        cfgs    = cfgfiles
#        if options.has_key("FeatureServerConfig"):
#            cfgs = (options["FeatureServerConfig"],) + cfgs
#        theServer = Server.load(*cfgs)
#    return mod_python(theServer.dispatchRequest, apacheReq)

def wsgi_app (environ, start_response):
    global theServer, lastRead
    last = 0
    for cfg in cfgfiles:
        try:
            cfgTime = os.stat(cfg)[8]
            if cfgTime > last:
                last = cfgTime
        except:
            pass        
    if not theServer or last > lastRead:
        cfgs      = cfgfiles
        theServer = Server.load(*cfgs)
        lastRead = time.time()
        
    return wsgi(theServer.dispatchRequest, environ, start_response)

def wsgi_app_workspace(environ, start_response):
    global theServer, lastRead
    last = 0
    for cfg in cfgfiles:
        try:
            cfgTime = os.stat(cfg)[8]
            if cfgTime > last:
                last = cfgTime
        except:
            pass        
    if not theServer or last > lastRead:
        cfgs      = cfgfiles
        theServer = Server.load(*cfgs)
        lastRead = time.time()
        
    return wsgi(theServer.dispatchWorkspaceRequest, environ, start_response)


if __name__ == '__main__':
    service = Server.load(*cfgfiles)
    cgi(service)
