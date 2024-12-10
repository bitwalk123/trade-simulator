from enum import Enum


class PositionType(Enum):
    UNKNOWN = 0
    NONE = 1
    #
    BUY = 2
    SELL = 3
    # wait for trend reversal
    BUY_POST = 4
    SELL_POST = 5


class ProfitType(Enum):
    UPDATE_MAX = 0
    SECURE_PROFIT = 1  # 利確
    KEEP = 2


class TrendType(Enum):
    NONE = 0
    SAME = 1
    OPPOSITE = 2
    NA = 3


class TypeDeal(Enum):
    BUYSELL = 1
    TRANSACTION = 2
    FORCE = 3


class XAxisRange(Enum):
    DAY = 1
    AM = 2
    PM = 3
