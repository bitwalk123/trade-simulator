from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractButton,
    QDockWidget,
    QWidget,
)

from structs.info import SimInfo
from widgets.buttons import TickerButton, ButtonGroup
from widgets.layouts import VBoxLayout


class DockSimulator(QDockWidget):
    tickerSelected = Signal(str)

    def __init__(self, info: SimInfo):
        super().__init__()
        self.info = info
        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )
        # _____________________________________________________________________
        # base container
        base = QWidget()
        self.setWidget(base)

        layout = VBoxLayout()
        base.setLayout(layout)

        self.but_ticker_group = but_ticker_group = ButtonGroup()
        but_ticker_group.buttonToggled.connect(self.on_ticker_selected)

        for key in info.getTickerKeys():
            but = TickerButton(key)
            but.setToolTip(info.getTickerValue(key))
            self.but_ticker_group.addButton(but)
            layout.addWidget(but)

        # _____________________________________________________________________
        # stretch
        layout.addStretch(stretch=1)

    def on_ticker_selected(self, button, state):
        if state:
            self.tickerSelected.emit(button.toolTip())

    def getTickerSelected(self) -> str | None:
        but: QAbstractButton = self.but_ticker_group.checkedButton()
        if but is not None:
            key = but.text()
            return self.info.getTickerValue(key)
        else:
            return None
