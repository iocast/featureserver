from OutputFormat import OutputFormat
from vectorformats.formats.csv import CSV as CSVFormat


class CSV(OutputFormat):
    def encode(self, results):
        csv = CSVFormat(layername=self.datasources[0])

        output = csv.encode(results)
        
        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.csv'
        }
        
        return ("application/octet-stream;", output, headers, '')

    def encode_exception_report(self, exceptionReport):
        csv = CSVFormat()
        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.csv'
        }
        return ("application/octet-stream;", csv.encode_exception_report(exceptionReport), headers, '')