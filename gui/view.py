import os
import json

from typing import Sequence
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLineEdit,
    QListView, QLabel, QDialogButtonBox, QPushButton,
    QFileDialog, QComboBox
)
from PySide6.QtCore import Qt, QModelIndex


from gui.models import TemplateModel, Template
from gui.gui import Dialog
from tools.tools import get_data
from tools.const import TMP


def get_templates(file) -> dict:
    with open(file, 'r') as fp:
        res = json.load(fp)
    return res


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None, flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        
        self.setWindowTitle('ANSYS Post Processing')

        self.__cdir = os.sep

        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)

        add_tmp_btn = QPushButton('Add Template')
        std_btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        std_btn.accepted.connect(self.accept)
        std_btn.rejected.connect(self.reject)
        add_tmp_btn.clicked.connect(self.add)

        self.tmpEdit = QLineEdit(self)
        self.tmpEdit.setPlaceholderText('Enter template name...')
        
        self.tmpView = QListView(self)
        self.tmpView.clicked.connect(self.setInfo)
        self.tmpModel = TemplateModel()
        self.tmpView.setModel(self.tmpModel)

        self.tmpCmb = QComboBox(self)
        self.tmpCmb.addItems(get_templates(TMP).keys())

        self.info = QLabel()

        layout.addWidget(self.tmpView, 0, 0)
        layout.addWidget(self.tmpCmb, 1, 0)
        layout.addWidget(self.tmpEdit, 2, 0)
        layout.addWidget(add_tmp_btn, 3, 0)
        layout.addWidget(self.info, 4, 0)
        layout.addWidget(std_btn, 5, 0)

        self.setCentralWidget(widget)

    def accept(self):
        pass
    
    def reject(self):
        pass

    def add(self):

        res_files = QFileDialog.getOpenFileNames(
            self, 'Add ANSYS res files...', self.__cdir, 'Ansys res (*.res)'
        )

        self.__cdir = os.path.split(res_files[0][0])[0]
        out_file = QFileDialog.getOpenFileName(
            self, 'Open ANSYS out file...', self.__cdir, 'ANSYS out (*.out)'
        )

        self.__cdir = os.path.split(out_file[0])[0]
        model = get_data(out_file[0])
        name = self.tmpEdit.text() if self.tmpEdit.text() else self.tmpCmb.currentText()

        object = get_templates(TMP)
        tmp = self.tmpCmb.currentText()
        dialog = Dialog(title=name, objects=object[tmp], model=model)
        dialog.show()
        dialog.exec()

        data = dialog.data
        
        if not data:
            return None
        
        template = Template(name=name, data=data, files=res_files[1])

        self.tmpModel.templates.append(template)
        self.tmpModel.layoutChanged.emit()

        self.tmpEdit.clear()
        self.tmpEdit.setPlaceholderText('Enter template name')

    def setInfo(self, index: QModelIndex):
        item = self.tmpModel.item(index)
        self.info.setText(item.info())
        
