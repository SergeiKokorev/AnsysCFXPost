import os
import json

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout,
    QDialogButtonBox, QPushButton,
    QFileDialog, QComboBox, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt


from gui.dialogues import TemplateDialog, TemplateTree
from tools.tools import get_data
from tools.const import TMP
from models.data import Templates


def get_templates(file) -> dict:
    with open(file, 'r') as fp:
        res = json.load(fp)
    return res


class DesignerView(QMainWindow):

    def __init__(self, parent=None, f=Qt.WindowType.Window):
        super(DesignerView, self).__init__(parent, f)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        add_widget_btn = QPushButton('+')
        add_widget_btn.clicked.connect(self.addWidget)

        layout.addWidget(add_widget_btn)
        self.setCentralWidget(widget)
    
    def addWidget(self):
        layout = self.centralWidget().layout()
        hbox = QHBoxLayout()

    def delWidget(self):
        pass

    def moveUp(self):
        pass

    def moveDown(self):
        pass

    def accept(self):
        pass

    def reject(self):
        pass


class PostView(QMainWindow):

    def __init__(self, parent: QWidget = None, flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super(PostView, self).__init__(parent, flags)
        
        self.setWindowTitle('ANSYS Post Processing')

        self.__cdir = os.sep
        self.__temp = Templates()
        self.__dmn = None

        with open(TMP, 'r') as fp:
            self.__templates = json.load(fp)

        layout = QGridLayout()

        dialog_btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        dialog_btn.accepted.connect(self.accept)
        dialog_btn.rejected.connect(self.reject)

        btn = QPushButton('Add template')
        btn.clicked.connect(self.add)

        self.tmpView = TemplateTree(parent=self, model=self.__temp)
        self.cmbTmp = QComboBox()
        self.cmbTmp.addItems(self.__templates.keys())
        self.tmpName = QLineEdit()
        self.tmpName.setPlaceholderText('Enter template name')

        layout.addWidget(self.tmpView, 0, 0)
        layout.addWidget(self.cmbTmp, 1, 0)
        layout.addWidget(self.tmpName, 2, 0)
        layout.addWidget(btn, 3, 0)
        layout.addWidget(dialog_btn, 4, 0, Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def accept(self):
        self.close()
    
    def reject(self):
        self.__temp = None
        self.close()

    def data(self):
        return self.__temp

    def add(self):
        out_file = QFileDialog.getOpenFileName(
            self, 'Open ANSYS out file', self.__cdir, 'ANSYS out (*.out)'
        )
        if not out_file[0]:
            return None
        
        self.__dmn = get_data(out_file[0])
        tmp = self.cmbTmp.currentText()
        name = self.tmpName.text() if self.tmpName.text() else tmp
        dialog = TemplateDialog(title=name, objects=self.__templates[tmp]['widgets'], model=self.__dmn, parent=self)
        dialog.exec()

        if not (data := dialog.data()):
            return None
        
        self.tmpView.addItem(data)
