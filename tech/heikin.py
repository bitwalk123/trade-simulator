import numpy as np
import pandas as pd


def get_heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    df_mean = df.copy()
    for col in df.columns:
        df_mean[col] = np.nan

    """
    【参考・引用サイト】
    https://marketspeed.jp/ms2/onlinehelp/ohm_007/ohm_007_05.html
    """
    for i, dt in enumerate(df.index):
        # 1本目の平均足
        # 前日の平均足がなく始値が算出出来ないため、描画対象外
        if i == 0:
            continue

        # 【平均足の始値】
        if i == 1:
            # 2本目の平均足：前日の平均足がないため、始値を下記値より算出する
            # 始値=(前日の始値+前日の高値+前日の安値+前日の終値)/4
            p_open = df.iloc[0].mean()
        else:
            # 始値=(前日の平均足の始値+前日の平均足の終値)/2
            p_open = df_mean.iloc[i - 1][['Open', 'Close']].mean()

        # 【平均足の終値】
        # 終値=(当日の始値+当日の高値+当日の安値+当日の終値)/4
        p_close = df.iloc[i].mean()

        """
        陰線：始値＞＝終値
        陽線：始値＜終値
        平均足の高値と安値は、当日の高値と安値を用いる。但し、
        平均足が陰線で当日の高値＜平均足の始値の場合、平均足の高値=平均足の始値とする。
        平均足が陽線で当日の安値＞平均足の始値の場合、平均足の安値=平均足の始値とする。
        """
        # 【平均足の高値】
        if p_open >= p_close:  # 平均足が陰線
            p_high = max(p_open, df.iloc[i]['High'])
        else:
            p_high = df.iloc[i]['High']

        # 【平均足の安値】
        if p_open < p_close:  # 平均足が陽線
            p_low = min(p_open, df.iloc[i]['Low'])
        else:
            p_low = df.iloc[i]['Low']

        df_mean.iloc[i] = [p_open, p_high, p_low, p_close]

    return df_mean
