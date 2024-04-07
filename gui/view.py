import os
import json

from typing import Sequence
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLineEdit,
    QListView, QLabel, QDialogButtonBox, QPushButton,
    QFileDialog, QComboBox, QButtonGroup
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
        self.__res_files = None
        self.__out_file = None
        self.addTmpBtnID = 2

        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)

        # Buttons
        self.add_tmp_btn = QPushButton('Add Template')
        self.add_tmp_btn.setEnabled(False)
        std_btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonGroup = QButtonGroup()

        self.buttonGroup.addButton(QPushButton('add res'), 0)
        self.buttonGroup.addButton(QPushButton('add out'), 1)
        self.buttonGroup.addButton(QPushButton('add template'), self.addTmpBtnID)
        self.buttonGroup.idClicked.connect(self.add)
        self.buttonGroup.button(2).setEnabled(False)

        self.tmpEdit = QLineEdit(self)
        self.tmpEdit.setPlaceholderText('Enter template name...')
        
        self.tmpView = QListView(self)
        self.tmpView.clicked.connect(self.setInfo)
        self.tmpModel = TemplateModel()
        self.tmpView.setModel(self.tmpModel)

        self.tmpCmb = QComboBox(self)
        self.tmpCmb.addItems(get_templates(TMP).keys())

        self.info = QLabel()

        layout.addWidget(self.tmpView, 0, 0, 1, 2)
        layout.addWidget(self.tmpCmb, 1, 0, 1, 2)
        layout.addWidget(self.tmpEdit, 2, 0, 1, 2)
        layout.addWidget(self.buttonGroup.button(0), 3, 0)
        layout.addWidget(self.buttonGroup.button(1), 3, 1)
        layout.addWidget(self.buttonGroup.button(2), 4, 0, 1, 2)
        layout.addWidget(self.info, 5, 0, 1, 2)
        layout.addWidget(std_btn, 6, 0, 1, 2)

        self.setCentralWidget(widget)

    def accept(self):
        pass
    
    def reject(self):
        pass

    def add_res(self):
        res = QFileDialog.getOpenFileNames(
            self, 'Add ANSYS res files...', self.__cdir, 'Ansys res (*.res)'
        )
        self.__cdir = os.path.split(res[0][0])[0]
        return res

    def add_out(self):
        out = QFileDialog.getOpenFileName(
            self, 'Open ANSYS out file...', self.__cdir, 'ANSYS out (*.out)'
        )
        if not out:
            return None
        
        self.__cdir = os.path.split(out[0])[0]
        self.add_tmp_btn.setEnabled(True)
        return out

    def add(self, buttonID: int):
        
        match buttonID:
            case 0:
                self.__res_files = QFileDialog.getOpenFileNames(
                    self, 'ANSYS res files...', self.__cdir, 
                    'ASYS res (*.res)'
                )
                self.__cdir = os.path.split(self.__res_files[0][0])[0]
            case 1:
                self.__out_file = QFileDialog.getOpenFileName(
                    self, 'ANSYS out file...', self.__cdir,
                    'ANSYS out (*.out)'
                )
                self.__cdir = os.path.split(self.__out_file[0])[0]
                self.buttonGroup.button(self.addTmpBtnID).setEnabled(True)
            case self.addTmpBtnID:
                self.buttonGroup.button(self.addTmpBtnID).setEnabled(False)
                model: List[Domain] = get_data(self.__out_file[0])
                template = self.tmpCmb.currentText()
                name = self.tmpEdit.text() if self.tmpEdit.text() else template
                obj = get_templates(TMP)
                dialog = Dialog(parent=self, title=name, objects=obj[template], model=model)
                dialog.exec()

                template = dialog.template

                if not template:
                    return None
                
                self.tmpModel.layoutChanged.emit()
                self.__res_files = None
                self.__out_file = None
                self.tmpModel.templates.append(template)
                self.tmpEdit.clear()
                self.tmpEdit.setPlaceholderText('Enter template name')
        
    def setInfo(self, index: QModelIndex):
        item = self.tmpModel.item(index)
        self.info.setText(item.info())
        
