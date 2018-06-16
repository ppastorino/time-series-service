from flask import Flask
from flask import request
import json
import pandas
import datetime
import numpy as np
from datasource import DataSourceManager
from flask_cors import CORS

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):

        print('DEBUG-Encoder')
        if isinstance(obj, pandas.Timestamp) or isinstance(obj, datetime) or isinstance(obj, np.datetime64):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


datasource_manager = DataSourceManager()
app = Flask(__name__)
CORS(app)
app.json_encoder = CustomEncoder

def build_data_frame(series_list):
    merge = None
    for s in series_list:
        print(s)
        if merge is None:
            merge = datasource_manager.get_data_frame(s)
        else:
            merge = pandas.merge(merge, datasource_manager.get_data_frame(s), on='d')

    merge.index = merge['d']
    del merge['d']
    merge.columns = series_list

    """ TODO utilizar parametros desde/hastsa """
    merge = merge['2017']
    if len(series_list) > 1:
        merge = (merge-merge.min())/(merge.max()-merge.min())

    print(merge)

    return merge


@app.route("/api/series/options", methods=['GET'])
def series_options():
    return json.dumps(series)


@app.route("/api/series/data", methods=['GET'])
def series_data():
    print(request.args.getlist("serie"))
    series_list = request.args.getlist("serie")
    data_frame = build_data_frame(series_list)

    values = []
    for s in series_list:
                values.append({"data": data_frame[s].values.tolist(), "label": s})
    response = {
                "index": data_frame.index.values.tolist(),
                "values": values
               }

    return json.dumps(response)
