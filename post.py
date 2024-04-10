import json
from PySide6.QtWidgets import QApplication


from gui.post_view import MainWindow


def main():

    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

    print(window.data())


if __name__ == "__main__":
    main()
