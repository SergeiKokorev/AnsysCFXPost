import json
from PySide6.QtWidgets import QApplication


from gui.views import PostView


def main():

    app = QApplication()
    window = PostView()
    window.show()
    app.exec()

    print(window.data())


if __name__ == "__main__":
    main()
