from __future__ import annotations

from PySide6.QtWidgets import (
    QLineEdit, QWidget, QComboBox,
    QWidget, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QIntValidator,QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression


from gui.dialogues import DomainDialog
from models.gui import ListModel


class IntLineEdit(QLineEdit):

    def __init__(self, parent=None) -> None:
        super(IntLineEdit, self).__init__(parent)
        validator = QIntValidator(self)
        self.setValidator(validator)

    def setModel(self, model=None):
        return None

    def data(self) -> int:
        return int(self.text() if self.text() else 0)


class DoubleLineEdit(QLineEdit):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        reg = QRegularExpression()
        reg.setPattern(r'[0-9]*\.{0, 1}[0-9]*')
        validator = QRegularExpressionValidator()
        validator.setRegularExpression(reg)
        self.setValidator(validator)

    def setModel(self, model=None):
        return None

    def data(self) -> float:
        return float(self.text()) if self.text() else 0.0


class InterfaceComboBox(QWidget):

    def __init__(self, *args, model=None, **kwargs) -> None:
        super(InterfaceComboBox, self).__init__(*args, **kwargs)

        self.tree_model = model
        self.list_model = model.listModel()
        list_model = ListModel(model=self.list_model)

        layout = QHBoxLayout()

        self.cmb = QComboBox()
        self.cmb.setModel(list_model)
        btn = QPushButton('...')
        btn.clicked.connect(self.popup)

        layout.addWidget(self.cmb)
        layout.addWidget(btn)

        self.setLayout(layout)

    def popup(self) -> None:

        tree = DomainDialog(model=self.tree_model)
        tree.show()
        tree.exec()
        if (item := str(tree.currentItem)):
            if self.cmb.findText(item): self.cmb.setCurrentText(item)
        return None
    
    def data(self):
        return self.cmb.currentText()
