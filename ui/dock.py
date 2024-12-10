from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QDockWidget,
    QVBoxLayout,
    QWidget,
)

from structs.info import SimInfo
from widgets.buttons import TickerButton


class DockSimulator(QDockWidget):
    tickerSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        info = SimInfo()
        # _____________________________________________________________________
        # base container
        base = QWidget()
        self.setWidget(base)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        base.setLayout(layout)

        self.but_ticker_group = but_ticker_group = QButtonGroup()
        but_ticker_group.buttonToggled.connect(self.on_ticker_selected)

        dict_ticker = info.ticker
        for key in dict_ticker.keys():
            but = TickerButton(key)
            but.setToolTip(dict_ticker[key])
            self.but_ticker_group.addButton(but)
            layout.addWidget(but)

        # _____________________________________________________________________
        # stretch
        layout.addStretch(stretch=1)

    def on_ticker_selected(self, button, state):
        if state:
            self.tickerSelected.emit(button.toolTip())
