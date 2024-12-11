from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractButton, QStyle

from structs.enumtype import ChartType
from structs.info import SimInfo
from widgets.buttons import (
    ButtonGroup,
    RadioButtonChartType,
    SpinBox,
    ToolButton, SpinBoxFloat,
)
from widgets.combos import ComboBox
from widgets.labels import LabelRight
from widgets.toolbars import ToolBar


class ToolBarSimulator(ToolBar):
    clickedPlay = Signal()

    def __init__(self, info: SimInfo):
        super().__init__()
        self.info = info

        # _____________________________________________________________________
        # チャート・タイプ
        lab_chart = LabelRight('チャート・タイプ')
        self.addWidget(lab_chart)

        self.rb_ctype_group = rb_ctype_group = ButtonGroup()
        rb_ctype_group.buttonToggled.connect(self.on_chart_type_changed)

        rb_candle = RadioButtonChartType('ローソク足')
        rb_candle.setChartType(ChartType.CANDLE)
        rb_candle.setChecked(True)
        info.setChartType(rb_candle.getChartType())
        rb_ctype_group.addButton(rb_candle)
        self.addWidget(rb_candle)

        rb_heikin = RadioButtonChartType('平均足')
        rb_heikin.setChartType(ChartType.HEIKIN)
        rb_ctype_group.addButton(rb_heikin)
        self.addWidget(rb_heikin)

        self.addSeparator()

        # _____________________________________________________________________
        # 足種
        lab_interval = LabelRight('足種')
        self.addWidget(lab_interval)

        self.combo_interval = combo_interval = ComboBox()
        combo_interval.addItems(info.getIntervalKeys())
        self.addWidget(combo_interval)

        self.addSeparator()

        # _____________________________________________________________________
        # ロスカット倍率（×呼値）
        lab_losscut = LabelRight('ロスカット倍率（× 呼値）')
        self.addWidget(lab_losscut)

        sb_losscut = SpinBox()
        sb_losscut.setRange(5, 50)
        sb_losscut.setSingleStep(5)
        sb_losscut.setValue(info.getLossCutMag())
        sb_losscut.valueChanged.connect(self.on_losscut_changed)
        self.addWidget(sb_losscut)

        # _____________________________________________________________________
        # 利益確定レベル（含み益の現在最大値 × レベル）
        lab_profit = LabelRight('利益確定レベル')
        self.addWidget(lab_profit)

        sb_profit = SpinBoxFloat()
        sb_profit.setDecimals(1)
        sb_profit.setRange(0.0, 1.0)
        sb_profit.setSingleStep(0.1)
        sb_profit.setValue(info.getFixProfitLevel())
        sb_profit.valueChanged.connect(self.on_profit_level_changed)
        self.addWidget(sb_profit)

        self.addSeparator()

        # _____________________________________________________________________
        # プロット
        self.but_play = but_play = ToolButton()
        but_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
        but_play.setToolTip('プロット')
        but_play.clicked.connect(self.clickedPlay.emit)
        self.addWidget(but_play)

    def get_builtin_icon(self, name) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon

    def getChartType(self) -> ChartType:
        but: QAbstractButton | RadioButtonChartType = self.rb_ctype_group.checkedButton()
        if but is not None:
            return but.getChartType()
        else:
            return ChartType.NONE

    def getInterval(self):
        key_interval = self.combo_interval.currentText()
        return self.info.getIntervalValue(key_interval)

    def on_chart_type_changed(self, rb: RadioButtonChartType, state: bool):
        if state:
            self.info.setChartType(rb.getChartType())

    def on_losscut_changed(self, mag: int):
        self.info.setLossCutMag(mag)

    def on_profit_level_changed(self, level: float):
        self.info.setFixProfitLevel(level)
