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
        tp = '1d' # Time Period
        ti = '1m' # Time Interval
        ticker = yf.Ticker(symbol)
        df_raw = ticker.history(period=tp, interval=ti)
        try:
            title = '%s (%s)' % (ticker.info['longName'], symbol)
        except KeyError:
            title = symbol

        df = parabolic_sar_yahoo(df_raw)
        # plot chart
        self.chart.plot(df, title)

        # evaluation for buy/sell
        obj = TradeSimulator(df)
        obj.start()

    def on_ticker_selected(self, symbol: str):
        self.do_evaluation(symbol)
