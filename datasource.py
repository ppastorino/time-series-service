import pandas
import requests
import logging

class FileDatasource:
    """" File based dataSource  (json format)"""

    def __init__(self, path):
        self._path = path

    def get_data_frame(self):
        return pandas.read_json(self._path, orient='records', typ='frame',
                               dtype={"d": "datetime64[ns]", "v": "float64"})


BCRA_URL_BASE = "http://api.estadisticasbcrax.com/"
BCRA_URL_DOLAR = BCRA_URL_BASE + "usd_of"
BCRA_URL_MERVAL = BCRA_URL_BASE + "merval"
BCRA_BEARER_TOKEN = "BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NTk0NzM1NzcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJwcGFzdG9yaW5vQGdtYWlsLmNvbSJ9.Gvo5BUpGaNV_uq0AbKtQpCtobVdQwg7ruRkMjFhjLBbyQIiPidw_OBxIMXeqfeVaK6M7De-Ixc458soirfPgMg"


class HttpDatasource:
    """" Http based dataSource """

    def __init__(self, url, bearer_token, fallback):
        self._url = url
        self._bearer_token = bearer_token
        self._fallback = fallback

    def get_data_frame(self):
        try:
            headers = {'Authorization': self._bearer_token}
            r = requests.get(self._url, headers=headers)
            r.raise_for_status()
            return pandas.read_json(r.text, orient='records', typ='frame',
                                    dtype={"d": "datetime64[ns]", "v": "float64"})
        except Exception as e:
            logging.exception("Error obteniendo datos desde " + self._url)

            if not (self._fallback is None):
                print("Retorna datos locales")
                return self._fallback.get_data_frame()
            else:
                raise e


class DataSourceManager:
    """ """
    def __init__(self):
        self._datasources = {
            "dolar.local" : FileDatasource("./data/usd.json"),
            "merval.local" : FileDatasource("./data/merval.json")
        }
        self._datasources["dolar"] = HttpDatasource(BCRA_URL_DOLAR, BCRA_BEARER_TOKEN, self._datasources["dolar.local"])
        self._datasources["merval"] = HttpDatasource(BCRA_URL_MERVAL, BCRA_BEARER_TOKEN, self._datasources["merval.local"])


    def get_datasource(self, ds_name):
        return self._datasources[ds_name]

    def get_data_frame(self, ds_name):
        return self.get_datasource(ds_name).get_data_frame()
