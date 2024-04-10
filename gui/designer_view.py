from PySide6.QtWidgets import (
    QMainWindow
)
from PySide6.QtCore import Qt



class Designer(QMainWindow):

    def __init__(self, parent=None, f=Qt.WindowType.Window):
        super(Designer, self).__init__(parent, f)
        self.setWindowModality(Qt.WindowModality.WindowModal)

    
    def addWidget(self):
        pass

    def delWidget(self):
        pass

    def moveUp(self):
        pass

    def moveDown(self):
        pass

    def accept(self):
        return super().accept()
    
    
