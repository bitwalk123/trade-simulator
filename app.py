import sys

from PySide6.QtWidgets import QApplication

from ui.main import MainSimulator


def main():
    app = QApplication(sys.argv)
    win = MainSimulator()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
