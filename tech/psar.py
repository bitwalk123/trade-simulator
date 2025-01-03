from collections import deque

import pandas as pd

from funcs.tide import get_lunch_times
from structs.enumtype import ChartType
from tech.heikin import get_heikin_ashi


class PSAR:
    def __init__(self, init_af=0.02, max_af=0.2, af_step=0.02):
        self.max_af = max_af
        self.init_af = init_af
        self.af = init_af
        self.af_step = af_step
        self.extreme_point = None
        self.high_price_trend = []
        self.low_price_trend = []
        self.high_price_window = deque(maxlen=2)
        self.low_price_window = deque(maxlen=2)

        # Lists to track results
        self.psar_list = []
        self.af_list = []
        self.ep_list = []
        self.high_list = []
        self.low_list = []
        self.trend_list = []
        self._num_days = 0

    def calcPSAR(self, high, low):
        if self._num_days >= 3:
            psar = self._calcPSAR()
        else:
            psar = self._initPSARVals(high, low)

        psar = self._updateCurrentVals(psar, high, low)
        self._num_days += 1

        return psar

    def _initPSARVals(self, high, low):
        if len(self.low_price_window) <= 1:
            self.trend = None
            self.extreme_point = high
            return None

        if self.high_price_window[0] < self.high_price_window[1]:
            self.trend = 1
            psar = min(self.low_price_window)
            self.extreme_point = max(self.high_price_window)
        else:
            self.trend = 0
            psar = max(self.high_price_window)
            self.extreme_point = min(self.low_price_window)

        return psar

    def _calcPSAR(self):
        prev_psar = self.psar_list[-1]
        if self.trend == 1:  # Up
            psar = prev_psar + self.af * (self.extreme_point - prev_psar)
            psar = min(psar, min(self.low_price_window))
        else:
            psar = prev_psar - self.af * (prev_psar - self.extreme_point)
            psar = max(psar, max(self.high_price_window))

        return psar

    def _updateCurrentVals(self, psar, high, low):
        if self.trend == 1:
            self.high_price_trend.append(high)
        elif self.trend == 0:
            self.low_price_trend.append(low)

        psar = self._trendReversal(psar, high, low)

        self.psar_list.append(psar)
        self.af_list.append(self.af)
        self.ep_list.append(self.extreme_point)
        self.high_list.append(high)
        self.low_list.append(low)
        self.high_price_window.append(high)
        self.low_price_window.append(low)
        self.trend_list.append(self.trend)

        return psar

    def _trendReversal(self, psar, high, low):
        # Checks for reversals
        reversal = False
        if self.trend == 1 and psar > low:
            self.trend = 0
            psar = max(self.high_price_trend)
            self.extreme_point = low
            reversal = True
        elif self.trend == 0 and psar < high:
            self.trend = 1
            psar = min(self.low_price_trend)
            self.extreme_point = high
            reversal = True

        if reversal:
            self.af = self.init_af
            self.high_price_trend.clear()
            self.low_price_trend.clear()
        else:
            if high > self.extreme_point and self.trend == 1:
                self.af = min(self.af + self.af_step, self.max_af)
                self.extreme_point = high
            elif low < self.extreme_point and self.trend == 0:
                self.af = min(self.af + self.af_step, self.max_af)
                self.extreme_point = low

        return psar


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# functions
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

def parabolic_sar(df: pd.DataFrame):
    indic = PSAR()
    df['PSAR'] = df.apply(
        lambda x: indic.calcPSAR(x['High'], x['Low']), axis=1
    )
    # Add supporting data
    df['EP'] = indic.ep_list
    df['Trend'] = indic.trend_list
    df['AF'] = indic.af_list


def parabolic_sar_yahoo(df: pd.DataFrame, ctype: ChartType) -> pd.DataFrame:
    # Parabolic SAR for morning and afternoon separately
    dt_noon1, dt_noon2 = get_lunch_times(df)
    # Morning session
    df1 = df[df.index <= dt_noon1].copy()
    # Afternoon session
    df2 = df[df.index >= dt_noon2].copy()

    if ctype == ChartType.CANDLE:
        return psar_yahoo_candle(df1, df2)
    elif ctype == ChartType.HEIKIN:
        return psar_yahoo_heikin(df1, df2)
    else:
        return pd.DataFrame()


def psar_yahoo_candle(df1, df2):
    # Morning session
    parabolic_sar(df1)

    # Afternoon session
    if len(df2) > 2:
        parabolic_sar(df2)
        # conbine morning and afternoon data
        df = pd.concat([df1, df2])
    else:
        df = df1

    return df


def psar_yahoo_heikin(df1, df2):
    df_raw = pd.concat([df1, df2])[['Open', 'High', 'Low', 'Close']]
    """
    平均足の終値は実価格ではないため、
    元の終値を控えておき、'Price' という列名で追加しておく。
    """
    close_price = df_raw['Close']
    df = get_heikin_ashi(df_raw)
    df['Price'] = close_price

    dt_noon1, dt_noon2 = get_lunch_times(df)

    # First Rwa is always NaN
    df0 = df[df.index == df.index[0]].copy()

    # Morning session
    df1 = df[(df.index > df.index[0]) & (df.index <= dt_noon1)].copy()
    parabolic_sar(df1)

    # Afternoon session
    df2 = df[df.index >= dt_noon2].copy()
    if len(df2) > 2:
        parabolic_sar(df2)
        # conbine morning and afternoon data
        df = pd.concat([df0, df1, df2])
    else:
        df = pd.concat([df0, df1])

    return df
