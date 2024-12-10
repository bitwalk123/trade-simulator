from PySide6.QtWidgets import (
    QButtonGroup,
    QPushButton,
    QRadioButton,
    QToolButton,
)

from structs.enumtype import ChartType


class ButtonGroup(QButtonGroup):
    def __init__(self, *args):
        super().__init__(*args)


class RadioButtonChartType(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.ctype = ChartType.NONE

    def getChartType(self)->ChartType:
        return self.ctype

    def setChartType(self, ctype: ChartType):
        self.ctype = ctype



class TickerButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 0.5em;
            }
        """)


class ToolButton(QToolButton):
    def __init__(self, *args):
        super().__init__(*args)
