import json

from PySide6.QtWidgets import QApplication, QDialogButtonBox


from tools.tools import get_data
from gui.view import MainWindow


def main():

    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
