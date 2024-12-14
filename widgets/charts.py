import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import mplfinance as mpf

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class ChartSimulator(FigureCanvas):
    fig = Figure()

    def __init__(self):
        super().__init__(self.fig)
        self.setFixedSize(1200, 600)

        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 12

        self.fig.subplots_adjust(
            top=0.95,
            bottom=0.05,
            left=0.07,
            right=0.995,
        )
        self.ax = self.fig.add_subplot(111)

    def clearAxes(self):
        self.ax.cla()

    def plot(self, df: pd.DataFrame, title: str):
        # Clear
        self.clearAxes()

        # Parabolic SAR
        df['bull'] = df.loc[df['Trend'] == 1]['PSAR']
        df['bear'] = df.loc[df['Trend'] == 0]['PSAR']
        apds = [
            mpf.make_addplot(
                df['bull'],
                type='scatter',
                marker='o',
                markersize=10,
                color='red',
                label='uptrend',
                ax=self.ax
            ),
            mpf.make_addplot(
                df['bear'],
                type='scatter',
                marker='o',
                markersize=10,
                color='blue',
                label='downtrend',
                ax=self.ax
            ),
        ]

        mpf.plot(
            df,
            type='candle',
            style='default',
            volume=False,
            addplot=apds,
            xrotation=0,
            ax=self.ax,
        )

        self.ax.set_title(title)
        self.ax.grid()

        # Refresh
        self.refreshDraw()

    def refreshDraw(self):
        self.fig.canvas.draw()


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
