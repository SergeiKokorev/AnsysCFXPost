from typing import List
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel
)
from PySide6.QtCore import Qt


from models.data import Domain


class MainWindow(QMainWindow):

    def __init__(self, model: List[Domain], parent: QWidget = None, flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        
        self.model = model
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
