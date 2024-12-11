from structs.enumtype import PositionType


class CreditVault:
    def __init__(self):
        self.position_type = None
        self.price = None
        self.unit = None
        self.profit_max = 0
        self.init_position()

    def getPositionType(self):
        return self.position_type

    def getProfit(self, price_now) -> tuple:
        if self.position_type == PositionType.BUY:
            action = '売埋'
            delta = (price_now - self.price) * self.unit
        elif self.position_type == PositionType.SELL:
            action = '買埋'
            delta = (self.price - price_now) * self.unit
        else:
            action = '不明'
            delta = 0.0

        if delta > self.profit_max:
            self.profit_max = delta

        # DEBUG
        """
        if delta - int(delta) > 0:
            print(
                '### 建玉 %f, 現在価格 %f, 株数 %f, 含損益 %f' % (
                    self.price, price_now, self.unit, delta
                )
            )
        """

        return action, delta

    def getProfitMax(self) -> float:
        return self.profit_max

    def hasPosition(self) -> bool:
        if self.price == 0:
            return False
        else:
            return True

    def init_position(self):
        """
        ポジションを初期状態にする
        :return:
        """
        self.position_type = PositionType.NONE
        self.init_position_common()

    def init_position_common(self):
        self.price = 0.0
        self.unit = 100.0
        self.profit_max = 0.0

    def init_position_for_wait(self):
        """
        トレンド転換前に利確・損切した場合、
        次のトレンド転換まで待ちの状態にするためポジションを「待ち」にする。
        :return:
        """
        if self.position_type == PositionType.BUY:
            self.position_type = PositionType.BUY_POST
        elif self.position_type == PositionType.SELL:
            self.position_type = PositionType.SELL_POST
        else:
            self.position_type = PositionType.UNKNOWN

        self.init_position_common()

    def repayment(self, price_now: float, reversal: bool = True) -> tuple[str, float]:
        """
        建玉返済
        :param price_now:
        :param reversal:
        :return:
        """
        action, delta = self.getProfit(price_now)

        # ポジションの初期化
        if reversal:
            # トレンド転換後
            self.init_position()
        else:
            # トレンド転換前
            self.init_position_for_wait()

        return action, delta

    def transaction(self, position_type: PositionType, current_price) -> str:
        """
        建玉取得
        :param position_type:
        :param current_price:
        :return:
        """
        if self.position_type == PositionType.NONE:
            if position_type == PositionType.BUY:
                action = '買建'
            elif position_type == PositionType.SELL:
                action = '売建'
            else:
                action = '不明'
            self.position_type = position_type
            self.price = current_price
        elif self.position_type == PositionType.BUY_POST:
            if position_type == PositionType.SELL:
                action = '売建'
                self.position_type = position_type
                self.price = current_price
            else:
                action = '不明'
        elif self.position_type == PositionType.SELL_POST:
            if position_type == PositionType.BUY:
                action = '買建'
                self.position_type = position_type
                self.price = current_price
            else:
                action = '不明'
        else:
            action = '不明'

        return action
