from OutputFormat import OutputFormat
import vectorformats.Formats.CSV


class CSV(OutputFormat):
    def encode(self, results):
        csv = vectorformats.Formats.CSV.CSV(layername=self.datasources[0])

        output = csv.encode(results)
        
        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.csv'
        }
        
        return ("application/octet-stream;", output, headers, '')

    def encode_exception_report(self, exceptionReport):
        csv = vectorformats.Formats.CSV.CSV()
        headers = {
            'Accept': '*/*',
            'Content-Disposition' : 'attachment; filename=poidownload.csv'
        }
        return ("application/octet-stream;", csv.encode_exception_report(exceptionReport), headers, '')