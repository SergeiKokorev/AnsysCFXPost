import os

from typing import List
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QCursor, QAction
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox,
    QTreeView, QMenu, QFileDialog
)


from tools.tools import generate_dialog
from models.data import Template, Templates, Domain
from models.gui import TreeModel
from tools.const import MVC_WIDGETS as mvc, WIDGETS as wg


class WidgetDialog(QDialog):

    def __init__(self, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Window) -> None:
        super(WidgetDialog, self).__init__(parent, f)
        widgets = None
        

class DomainDialog(QDialog):

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
        index = self.tree.currentIndex()
        self.currentItem = self.model.childItem(index)
        return super().accept()

    def reject(self):
        self.currentItem = None
        return super().reject()


class TemplateDialog(QDialog):

    def __init__(self, title: str, objects: dict, model, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, f)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        self.objects = objects
        self.__template = Template(name=title)
        self.title = title

        layout = QVBoxLayout()

        self.setWindowTitle(title)
        
        btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)

        layout.addLayout(generate_dialog(objects, model, self))
        layout.addWidget(btn)
        self.setLayout(layout)

    def data(self):
        return self.__template

    def accept(self):

        tmp_data = dict([(w['name'], None) for w in self.objects])
        self.__template = Template(name=self.title, data=tmp_data)
        widgets = {**mvc, **wg}

        for widget in self.objects:
            child = self.findChild(widgets[widget['widget']], widget['name'])
            if child: self.__template.data[widget['name']] = (widget['title'], child.data())

        return super().accept()
    
    def reject(self):
        self.__template = None
        return super().reject()


class TemplateTree(QTreeView):

    def __init__(self, *args, model: Templates = None, **kwargs):

        super(TemplateTree, self).__init__(*args, **kwargs)
        
        self._model: TreeModel =TreeModel(model=model)
        self.__cdir = os.sep

        self.setModel(self._model)
        self.setHeaderHidden(True)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def addChildren(self):
        items = QFileDialog.getOpenFileNames(
            self, 'Add ANSYS res files', self.__cdir, 'ANSYS res (*.res)'
        )[0]
        
        if not len(items):
            return None
        
        self.__cdir = os.path.split(items[0])[0]
        index = self.currentIndex()
        self._model.addChildren(index, items)

    def addItem(self, item: Template):
        self._model.addItem(item)

    def delChild(self):
        index = self.currentIndex()
        self._model.delChild(index)

    def delItem(self):
        index = self.currentIndex()
        self._model.delItem(index)

    def mousePressEvent(self, event: QMouseEvent) -> None:

        if event.button() == Qt.MouseButton.RightButton:
            
            menu = QMenu()
            action1 = QAction('Add files')
            action2 = QAction('Delete file')
            action3 = QAction('Delete template')
            action1.triggered.connect(self.addChildren)
            action2.triggered.connect(self.delChild)
            action3.triggered.connect(self.delItem)
            menu.addAction(action1)
            menu.addAction(action2)
            menu.addAction(action3)

            if not self._model.rowCount():
                for action in menu.actions():
                    action.setEnabled(False)

            pos = self.mapToParent(QCursor.pos())
            menu.exec(pos)
        else:
            return super(TemplateTree, self).mousePressEvent(event)
