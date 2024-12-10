import os
from dataclasses import dataclass

from funcs.common import read_json
from structs.res import AppRes


@dataclass
class SimInfo:
    dict_interval = {
        '１分足': '1m',
        '２分足': '2m',
        '５分足': '5m',
    }

    def __init__(self):
        res = AppRes()
        conf_ticker = 'ticker.json'
        json_ticker = os.path.join(res.getConfigDir(), conf_ticker)
        self.dict_ticker = read_json(json_ticker)

        info_tick = 'tick_price.csv'
        self.tick_file = os.path.join(res.getInfoDir(), info_tick)

    def getIntervalKeys(self) -> list:
        return list(self.dict_interval.keys())

    def getIntervalValue(self, key: str) -> str:
        return self.dict_interval[key]

    def getTickFile(self) -> str:
        return self.tick_file

    def getTickerKeys(self) -> list:
        return list(self.dict_ticker.keys())

    def getTickerValue(self, key: str) -> str:
        return self.dict_ticker[key]
