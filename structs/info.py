import os
from dataclasses import dataclass

from funcs.common import read_json
from structs.res import AppRes


@dataclass
class SimInfo:
    def __init__(self):
        res = AppRes()
        conf_ticker = 'ticker.json'
        json_ticker = os.path.join(res.getConfigDir(), conf_ticker)
        self.ticker = read_json(json_ticker)

        info_tick = 'tick_price.csv'
        self.tick_file = os.path.join(res.getInfoDir(), info_tick)

    def getTickFile(self) -> str:
        return self.tick_file
