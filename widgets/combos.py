from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self, *args):
        super().__init__(*args)

