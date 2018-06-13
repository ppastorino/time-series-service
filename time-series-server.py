from flask import Flask
from flask import request
import json
import pandas
import datetime
import numpy as np

print("HELLO")

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):

        print('DEBUG-Encoder')
        if isinstance(obj, pandas.Timestamp) or isinstance(obj, datetime) or isinstance(obj, np.datetime64):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomEncoder

usd = pandas.read_json('./data/usd.json', orient='records', typ='frame',
                       dtype={"d": "datetime64[ns]", "v": "float64"})


merval = pandas.read_json('./data/merval.json', orient='records', typ='frame',
                          dtype={"d": "datetime64[ns]", "v": "float64"})

series = ["dolar", "merval"]

merge = pandas.merge(usd, merval, on='d')
merge.index = merge['d']
del merge['d']
merge.columns = ['dolar', 'merval']
merge = merge['2017']
merge = (merge-merge.min())/(merge.max()-merge.min())


@app.route("/api/series/options", methods=['GET'])
def seriesOptions():
    return json.dumps(series)


@app.route("/api/series/data", methods=['GET'])
def seriesData():
    print(request.args.getlist("serie"))
    response = {
                "index": merge.index.values.tolist(),
                "values":
                [
                    {"data": merge['dolar'].values.tolist(), "label": "dolar"},
                    {"data": merge['merval'].values.tolist(), "label": "merval"}
                ]
               }
    return json.dumps(response)
