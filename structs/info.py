import os
from dataclasses import dataclass

from funcs.common import read_json
from structs.enumtype import ChartType
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

        # チャートタイプ
        self.ctype = ChartType.NONE

        # ロスカットの倍率
        self.mag = 5

        # 利益確定レベル
        self.fix_profit_level = 0.8

    def getChartType(self) -> ChartType:
        return self.ctype

    def getFixProfitLevel(self) -> float:
        return self.fix_profit_level

    def getIntervalKeys(self) -> list:
        return list(self.dict_interval.keys())

    def getIntervalValue(self, key: str) -> str:
        return self.dict_interval[key]

    def getLossCutMag(self) -> int:
        return self.mag

    def getTickFile(self) -> str:
        return self.tick_file

    def getTickerKeys(self) -> list:
        return list(self.dict_ticker.keys())

    def getTickerValue(self, key: str) -> str:
        return self.dict_ticker[key]

    def setChartType(self, ctype: ChartType):
        self.ctype = ctype

    def setFixProfitLevel(self, level: float):
        self.fix_profit_level = level

    def setLossCutMag(self, mag: int):
        self.mag = mag
