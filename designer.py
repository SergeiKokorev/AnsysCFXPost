from PySide6.QtWidgets import QApplication


from gui.designer_view import Designer


def main():

    app = QApplication()
    designer = Designer()


    designer.show()
    app.exec()


if __name__ == "__main__":

    main()
