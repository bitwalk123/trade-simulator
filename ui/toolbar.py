from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle, QAbstractButton

from structs.enumtype import ChartType
from structs.info import SimInfo
from widgets.buttons import ToolButton, ButtonGroup, RadioButtonChartType
from widgets.combos import ComboBox
from widgets.labels import LabelRight
from widgets.toolbars import ToolBar


class ToolBarSimulator(ToolBar):
    clickedPlay = Signal()

    def __init__(self, info: SimInfo):
        super().__init__()
        self.info = info

        lab_chart = LabelRight('チャート')
        self.addWidget(lab_chart)

        self.rb_ctype_group = rb_ctype_group = ButtonGroup()

        rb_candle = RadioButtonChartType('ローソク足')
        rb_candle.setChartType(ChartType.CANDLE)
        rb_candle.setChecked(True)
        rb_ctype_group.addButton(rb_candle)
        self.addWidget(rb_candle)

        rb_heikin = RadioButtonChartType('平均足')
        rb_heikin.setChartType(ChartType.HEIKIN)
        rb_ctype_group.addButton(rb_heikin)
        self.addWidget(rb_heikin)

        self.addSeparator()
        lab_interval = LabelRight('足種')
        self.addWidget(lab_interval)

        self.combo_interval = combo_interval = ComboBox()
        combo_interval.addItems(info.getIntervalKeys())
        self.addWidget(combo_interval)

        self.addSeparator()
        self.but_play = but_play = ToolButton()
        but_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
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
