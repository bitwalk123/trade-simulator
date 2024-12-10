from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)


class LabelRight(Label):
    def __init__(self, *args):
        super().__init__(*args)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("""
            QLabel {
                padding: 0 1em 0 0.2em;
            }
        """)
