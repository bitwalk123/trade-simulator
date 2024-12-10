from PySide6.QtWidgets import QPushButton


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
