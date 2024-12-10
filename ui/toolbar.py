from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QStyle

from widgets.toolbars import ToolBar


class ToolBarSimulator(ToolBar):
    clickedPlay = Signal()

    def __init__(self):
        super().__init__()

        self.but_play = but_play = QToolButton()
        but_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
        but_play.clicked.connect(self.clickedPlay.emit)
        self.addWidget(but_play)

    def get_builtin_icon(self, name) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon
