import numpy as np
import pandas as pd

from sim.vault import CreditVault
from structs.enumtype import (
    PositionType,
    TrendType, ChartType,
)
from structs.info import SimInfo


def is_same_psar_trend(credit: CreditVault, trend: int) -> TrendType:
    if np.isnan(trend):
        return TrendType.NA
    # trend - 0: sell, 1: buy
    if trend == 0:
        if credit.position_type == PositionType.SELL:
            return TrendType.SAME
        elif credit.position_type == PositionType.SELL_POST:
            return TrendType.SAME
        else:
            return TrendType.OPPOSITE
    elif trend == 1:
        if credit.position_type == PositionType.BUY:
            return TrendType.SAME
        if credit.position_type == PositionType.BUY_POST:
            return TrendType.SAME
        else:
            return TrendType.OPPOSITE
    else:
        return TrendType.NONE


def get_losscut(df: pd.DataFrame, credit: CreditVault, mag: int, info: SimInfo) -> float:
    if info.getChartType() == ChartType.HEIKIN:
        price_mean = df['Price'].mean()
    else:
        price_mean = df['Close'].mean()
    df_tick = pd.read_csv(SimInfo().getTickFile())
    tick = df_tick[df_tick['Price'] > price_mean].head(1)['TOPIX'].iloc[0]
    losscut = -tick * mag * credit.unit
    return losscut


def get_row_data(df: pd.DataFrame, r: int, info: SimInfo):
    series = df.iloc[r]
    dt = series.name
    if info.getChartType() == ChartType.HEIKIN:
        price = series['Price']
    else:
        price = series['Close']
    trend = series['Trend']
    psar = series['PSAR']
    return dt, price, trend, psar


def get_trend_signal(trend: int) -> PositionType:
    if trend == 0:
        return PositionType.SELL
    elif trend == 1:
        return PositionType.BUY
    else:
        return PositionType.NONE
