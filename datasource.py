import pandas


class FileDatasource:
    """" File based dataSource  (json format)"""

    def __init__(self, path):
        self._path = path

    def get_data_frame(self):
        return pandas.read_json(self._path, orient='records', typ='frame',
                               dtype={"d": "datetime64[ns]", "v": "float64"})

class DataSourceManager:
    """ """


    def __init__(self):
        self._datasources = {
            "dolar" : FileDatasource("./data/usd.json"),
            "merval" : FileDatasource("./data/merval.json")
        }

    def get_datasource(self, ds_name):
        return self._datasources[ds_name]

    def get_data_frame(self, ds_name):
        return self.get_datasource(ds_name).get_data_frame()
