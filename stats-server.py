import http.server
import socketserver
import re
import json
import pandas
import datetime
import numpy as np
import os

PORT = int(os.environ.get('PORT', "8080"))

stat = {"age": 25}

usd = pandas.read_json('./data/usd.json', orient='records', typ='frame',
                       dtype={"d": "datetime64[ns]", "v": "float64"})


merval = pandas.read_json('./data/merval.json', orient='records', typ='frame',
                          dtype={"d": "datetime64[ns]", "v": "float64"})

merge = pandas.merge(usd, merval, on='d')
merge.index = merge['d']
del merge['d']
merge.columns = ['dolar', 'merval']
merge = merge['2017']

merge = (merge-merge.min())/(merge.max()-merge.min())

# response = {"columns": merge.columns, "index": merge.reset_index()}
print(merge.columns)
# TODO: Usar un encoder (en vez de toList) y generalizar esto
response = {
            "index": merge.index.values.tolist(),
            "values":
            [
                {"data": merge['dolar'].values.tolist(), "label": "dolar"},
                {"data": merge['merval'].values.tolist(), "label": "merval"}
            ]
           }


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pandas.Timestamp) or isinstance(obj, datetime) or isinstance(obj, np.datetime64):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


# s = pandas.Series(merge.values.tolist(), index=merge.columns)
# print(s.to_json())

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Servidor de estadisticas"""

    def do_GET(self):
        """Informa estadisticas"""

        if re.search('/api/v1/stat/*', self.path) is not None:
            recordID = self.path.split('/')[-1]
            stat['id'] = recordID
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
#           self.wfile.write(merge.to_json(orient='split', date_format='iso').encode("utf-8"))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


Handler = HTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
