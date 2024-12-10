import os
import yfinance as yf

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from structs.info import SimInfo
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

        info = SimInfo()
        # _____________________________________________________________________
        # Top toolbar
        self.toolbar = toolbar = ToolBarSimulator(info)
        toolbar.clickedPlay.connect(self.on_redo_evaluation)
        self.addToolBar(
            Qt.ToolBarArea.TopToolBarArea,
            toolbar,
        )

        # _____________________________________________________________________
        # monitor dock
        self.dock = dock = DockSimulator(info)
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
        tp = '1d' # Time Period, fixed for day trading
        ti = self.toolbar.getInterval() # Time Interval
        ticker = yf.Ticker(symbol)
        df_raw = ticker.history(period=tp, interval=ti)
        try:
            title = '%s (%s)' % (ticker.info['longName'], symbol)
        except KeyError:
            title = symbol

        df = parabolic_sar_yahoo(df_raw, self.toolbar.getChartType())
        # plot chart
        self.chart.plot(df, title)

        # evaluation for buy/sell
        obj = TradeSimulator(df)
        obj.start()

    def on_ticker_selected(self, symbol: str):
        self.do_evaluation(symbol)

    def on_redo_evaluation(self):
        symbol = self.dock.getTickerSelected()
        if symbol is not None:
            self.do_evaluation(symbol)
