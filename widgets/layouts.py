from PySide6.QtWidgets import QVBoxLayout


class VBoxLayout(QVBoxLayout):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(2, 2, 2, 2)
        self.setSpacing(2)
