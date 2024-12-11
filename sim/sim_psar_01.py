import pandas as pd
from PySide6.QtCore import QObject

from funcs.tide import get_lunch_times
from sim.common import (
    get_losscut,
    get_row_data,
    get_trend_signal,
    is_same_psar_trend,
)
from sim.vault import CreditVault
from structs.enumtype import (
    PositionType,
    TrendType,
)
from structs.info import SimInfo


class TradeSimulator(QObject):
    __name__ = 'SIM_PSAR_01'
    __version__ = '0.0.5'

    def __init__(self, df: pd.DataFrame, info: SimInfo):
        super().__init__()
        self.df = df
        self.info = info
        # 前場と後場で分ける
        self.dt_noon1, self.dt_noon2 = get_lunch_times(df)
        # 収益（グローバル）
        self.earning = 0

    def loop(self, df: pd.DataFrame) -> float:
        """
        ループ処理
        一行ずつデータフレームを読み込んで処理する
        :param df:
        :return:
        """
        # 建玉保持用オブジェクト
        credit = CreditVault()

        # ロスカット
        losscut = get_losscut(df, credit, mag=self.info.getLossCutMag())
        level_profit = self.info.getFixProfitLevel()
        print(
            '（ロスカット = %+.1f, 利確レベル = %.1f）' % (losscut, level_profit)
        )

        # 収益（ローカル）
        earning = 0

        # デバッグ・フラグ
        debug = False

        n = len(df)
        for r in range(n - 1):
            # -----------------------------------------------------------------
            # ループ処理の開始
            dt, price, trend, psar = get_row_data(df, r)
            # 含益
            _, gain = credit.getProfit(price)
            # トレンド転換かどうかの確認
            result = is_same_psar_trend(credit, trend)
            if credit.hasPosition():
                # 建玉を持っている場合
                # -------------------------------------------------------------
                if result == TrendType.OPPOSITE:
                    # PSAR がトレンド転換した場合
                    # ⇨ 建玉の返済処理
                    profit_max = credit.getProfitMax()
                    action, delta = credit.repayment(price)
                    # print('%s %s %.1f %+.1f' % (dt, action, price, delta))
                    print(
                        '%s %s %.1f %+.1f ｟最大含益 %+.1f｠' % (
                            dt, action, price, delta, profit_max
                        )
                    )
                    earning += delta
                elif result == TrendType.SAME:
                    # PSAR が同じトレンドの場合
                    profit_max = credit.getProfitMax()
                    if gain <= losscut:
                        # 損切
                        action, delta = credit.repayment(price, reversal=False)
                        print(
                            '%s %s %.1f %+.1f （損切）｟最大含益 %+.1f｠' % (
                                dt, action, price, delta, profit_max
                            )
                        )
                        earning += delta
                    elif (profit_max > 0) and (gain < profit_max * level_profit):
                        # 利確
                        action, delta = credit.repayment(price, reversal=False)
                        print(
                            '%s %s %.1f %+.1f （利確）｟最大含益 %+.1f｠' % (
                                dt, action, price, delta, profit_max
                            )
                        )
                        earning += delta
                    else:
                        if debug:
                            print('%s 含益 %.1f %+.1f' % (dt, price, gain))
                else:
                    if debug:
                        print('%s 無１ %.1f %+.1f' % (dt, price, gain))
            else:
                # 建玉を持っていない場合
                # -------------------------------------------------------------
                trend_signal = get_trend_signal(trend)
                if trend_signal != PositionType.NONE:
                    if credit.position_type == PositionType.NONE:
                        # PSAR のトレンドに従って建玉取得
                        action = credit.transaction(trend_signal, price)
                        print('%s %s %.1f' % (dt, action, price))
                    elif ((credit.position_type == PositionType.BUY_POST) or (
                            credit.position_type == PositionType.SELL_POST)) and (result == TrendType.OPPOSITE):
                        # PSAR のトレンドに従って建玉取得
                        action = credit.transaction(trend_signal, price)
                        print('%s %s %.1f ※' % (dt, action, price))
                    else:
                        if debug:
                            print('%s 無２ %.1f %+.1f' % (dt, price, gain))
                else:
                    if debug:
                        print('%s 無３ %.1f %+.1f' % (dt, price, gain))

            # ループ処理の終了
            # -----------------------------------------------------------------

        # _____________________________________________________________________
        # 最後の行で強制決済
        r = n - 1
        dt, price, trend, _ = get_row_data(df, r)
        if credit.hasPosition():
            action, delta = credit.repayment(price)
            print('%s %s %.1f %+.1f （強制決済）' % (dt, action, price, delta))
            earning += delta

        return earning

    def start(self):
        # 前場と後場に分けて処理
        df1 = self.df[self.df.index <= self.dt_noon1]
        df2 = self.df[self.df.index >= self.dt_noon2]

        for i, df in enumerate([df1, df2]):
            if len(df) == 0:
                continue
            if i == 0:
                print('前場')
            else:
                print('\n後場')

            earning = self.loop(df)
            print('収益 %+.1f' % earning)
            self.earning += earning

        print('---')
        print('総収益 %+.1f' % self.earning)
        print('generated by %s %s' % (self.__name__, self.__version__))
