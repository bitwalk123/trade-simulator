import os
import yfinance as yf

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from tech.psar import parabolic_sar_yahoo
from sim.sim_psar_01 import TradeSimulator
from ui.dock import DockSimulator
from ui.toolbar import ToolBarSimulator
from widgets.charts import ChartSimulator, ChartNavigation


class MainSimulator(QMainWindow):
    __appname__ = 'シミュレータ'
    __version__ = '0.0.1'

    def __init__(self):
        super().__init__()

        # _____________________________________________________________________
        # title
        self.setWindowTitle('%s - %s' % (self.__appname__, self.__version__,))

        # _____________________________________________________________________
        # Top toolbar
        self.toolbar = toolbar = ToolBarSimulator()
        self.addToolBar(
            Qt.ToolBarArea.TopToolBarArea,
            toolbar,
        )

        # _____________________________________________________________________
        # monitor dock
        self.dock = dock = DockSimulator()
        dock.tickerSelected.connect(self.on_ticker_selected)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock
        )

        # _____________________________________________________________________
        # main window
        self.chart = chart = ChartSimulator()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Bottom toolbar
        self.navtoolbar = navtoolbar = ChartNavigation(chart)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

    def do_evaluation(self, symbol: str):
        ticker = yf.Ticker(symbol)
        df_1m = ticker.history(period='1d', interval='1m')
        try:
            title = '%s (%s)' % (ticker.info['longName'], symbol)
        except KeyError:
            title = symbol
        df_1m = parabolic_sar_yahoo(df_1m)

        # plot chart
        self.chart.plot(df_1m, title)

        # evaluation for buy/sell
        obj = TradeSimulator(df_1m)
        obj.start()

    def on_ticker_selected(self, symbol: str):
        self.do_evaluation(symbol)
