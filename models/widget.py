from PySide6.QtWidgets import (
    QLineEdit, QTreeView, QWidget, QComboBox,
    QWidget, QHBoxLayout, QPushButton, QDialog,
    QDialogButtonBox, QVBoxLayout
)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt, QLocale


from models.gui import *


class PopupDomainTree(QDialog):

    def __init__(self, model: List[Domain] = None, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, f)

        self.model = TreeModel(model=model)
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setModel(self.model)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.tree.doubleClicked.connect(self.accept)
        self.currentItem = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)
        layout.addWidget(self.tree)
        layout.addWidget(btn)

    def accept(self) -> None:
        self.currentItem = self.model.childItem(self.tree.currentIndex())
        return super().accept()

    def reject(self):
        self.currentItem = None
        return super().reject()


class IntLineEdit(QLineEdit):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        validator = QIntValidator(self)
        self.setValidator(validator)

    def data(self) -> int:
        return int(self.text() if self.text() else 0)


class DoubleLineEdit(QLineEdit):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        validator = QDoubleValidator(self)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setLocale(locale)
        self.setValidator(validator)

    def data(self) -> float:
        return float(self.text().replace(',', '.') if self.text() else 0.0)


class InterfaceComboBox(QWidget):

    def __init__(self, *args, model: List[Domain], **kwargs) -> None:
        super(InterfaceComboBox, self).__init__(*args, **kwargs)

        self.model = model
        list_model = ListModel(model=model)

        layout = QHBoxLayout()

        self.cmb = QComboBox()
        self.cmb.setModel(list_model)

        btn = QPushButton('...')
        btn.clicked.connect(self.popup)

        layout.addWidget(self.cmb)
        layout.addWidget(btn)

        self.setLayout(layout)

    def popup(self) -> None:

        tree = PopupDomainTree(model=self.model)
        tree.show()
        tree.exec()
        if (item := str(tree.currentItem)):
            if self.cmb.findText(item): self.cmb.setCurrentText(item)
        return None
    
    def data(self):
        return self.cmb.currentText()
