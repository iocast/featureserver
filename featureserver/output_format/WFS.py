
from OutputFormat import OutputFormat
from ..parsers.web_feature_service.response.transaction import TransactionResponse

from ..vectorformats.wfs import WFS as WFSFormat

class WFS(OutputFormat):
    def encode(self, results):
        wfs = WFSFormat(self.service)
        
        if isinstance(results, TransactionResponse):
            return ("text/xml", self.encode_transaction(results), None, 'utf-8')
        
        output = wfs.encode(results)
        return ("text/xml", output, None, 'utf-8')
    
    def get_capabilities(self):
        wfs = WFSFormat(service=self.service)
        return ("text/xml", wfs.get_capabilities(), None, 'utf-8')
    
    def describe_feature_type(self):
        wfs = WFSFormat(service=self.service)
        return ("text/xml; subtype=gml/3.1.1", wfs.describe_feature_type(), None, 'utf-8')



    def encode_exception_report(self, exceptionReport):
        results = ["""<?xml version="1.0" encoding="UTF-8"?>
            <ExceptionReport xmlns="http://www.opengis.net/ows/1.1"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.opengis.net/ows/1.1 owsExceptionReport.xsd"
            version="1.0.0"
            xml:lang="en">
            """]
        for exception in exceptionReport:
            results.append("<Exception exceptionCode=\"%s\" locator=\"%s\" layer=\"%s\"><ExceptionText>%s</ExceptionText><ExceptionDump>%s</ExceptionDump></Exception>" % (exception.code, exception.locator, exception.layer, exception.message, exception.dump))
        results.append("""</ExceptionReport>""")
        out = "\n".join(results)
    
        return ("text/xml", out, None, 'utf-8')
    
    def encode_transaction(self, response, **kwargs):
        failedCount = 0
        
        summary = response.summary
        result = """<?xml version="1.0" encoding="UTF-8"?>
            <wfs:TransactionResponse version="1.1.0"
            xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-transaction.xsd"
            xmlns:og="http://opengeo.org"
            xmlns:ogc="http://www.opengis.net/ogc"
            xmlns:tiger="http://www.census.gov"
            xmlns:cite="http://www.opengeospatial.net/cite"
            xmlns:nurc="http://www.nurc.nato.int"
            xmlns:sde="http://geoserver.sf.net"
            xmlns:analytics="http://opengeo.org/analytics"
            xmlns:wfs="http://www.opengis.net/wfs"
            xmlns:topp="http://www.openplans.org/topp"
            xmlns:it.geosolutions="http://www.geo-solutions.it"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:sf="http://www.openplans.org/spearfish"
            xmlns:ows="http://www.opengis.net/ows"
            xmlns:gml="http://www.opengis.net/gml"
            xmlns:za="http://opengeo.org/za"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:tike="http://opengeo.org/#tike">
            <wfs:TransactionSummary>
            <wfs:totalInserted>%s</wfs:totalInserted>
            <wfs:totalUpdated>%s</wfs:totalUpdated>
            <wfs:totalDeleted>%s</wfs:totalDeleted>
            <wfs:totalReplaced>%s</wfs:totalReplaced>
            </wfs:TransactionSummary>
            <wfs:TransactionResults/> """ % (str(summary.inserts), str(summary.updates), str(summary.deletes), str(summary.replaces))
        
        result += "<wfs:InsertResults>"
        for insert in response.inserts:
            result += """<wfs:Feature handle="%s">""" % str(insert.handle)
            for id in insert:
                result += """<ogc:ResourceId fid="%s"/>""" % str(id)
            result += """</wfs:Feature>"""
            if len(insert.handle) > 0:
                failedCount += 1
        result += """</wfs:InsertResults>"""
        
        result += "<wfs:UpdateResults>"
        for update in response.updates:
            result += """<wfs:Feature handle="%s">""" % str(update.handle)
            for id in update:
                result += """<ogc:ResourceId fid="%s"/>""" % str(id)
            result += """</wfs:Feature>"""
            if len(update.handle) > 0:
                failedCount += 1
        result += """</wfs:UpdateResults>"""
        
        result += "<wfs:ReplaceResults>"
        for replace in response.replaces:
            result += """<wfs:Feature handle="%s">""" % str(replace.handle)
            for id in replace:
                result += """<ogc:ResourceId fid="%s"/>""" % str(id)
            result += """</wfs:Feature>"""
            if len(replace.handle) > 0:
                failedCount += 1
        result += """</wfs:ReplaceResults>"""
        
        result += "<wfs:DeleteResults>"
        for delete in response.replaces:
            result += """<wfs:Feature handle="%s">""" % str(delete.handle)
            for id in delete:
                result += """<ogc:ResourceId fid="%s"/>""" % str(id)
            result += """</wfs:Feature>"""
            if len(delete.handle) > 0:
                failedCount += 1
        result += """</wfs:DeleteResults>"""
        
        
        result += """<wfs:TransactionResult>
            <wfs:Status> """
        
        if (len(response.inserts) + len(response.updates) + len(response.replaces) + len(response.deletes)) == failedCount:
            result += "<wfs:FAILED/>"
        elif (len(response.inserts) + len(response.updates) + len(response.replaces) + len(response.deletes)) > failedCount and failedCount > 0:
            result += "<wfs:PARTIAL/>"
        else:
            result += "<wfs:SUCCESS/>"


        result += """</wfs:Status>
            </wfs:TransactionResult>"""


        result += """</wfs:TransactionResponse>"""

        return result


