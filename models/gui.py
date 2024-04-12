from typing import Any, List
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


from models.data import Domains, Templates, Domain, Boundary, Template


class ListModel(QAbstractListModel):

    def __init__(self, *args, **kwargs) -> None:
        super(ListModel, self).__init__(*args, **kwargs)
        self.model: List[Boundary | Template] = None

    def setModel(self, model: List[Boundary | Template]):
        self.model = model

    def rowCount(self, parent: QModelIndex=None) -> int:
        return self.model.rowCount()
    
    def columnCount(self, parent: QModelIndex=None) -> int:
        return 1
    
    def data(self, index: QModelIndex, role: int = ...) -> Any:
        
        if not index.isValid():
            return None
        
        if not 0 <= index.row() <= self.rowCount():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.model.item(index.row()))


class TreeModel(QStandardItemModel):
    
    def __init__(self, *args, **kwargs):
        super(TreeModel, self).__init__(*args, **kwargs)
        self.model: Domains | Templates = None

    def setModel(self, model: List[Domains | Templates]):
        self.model = model
        self.update(model)

    def update(self, model):
        for row, i in enumerate(model.items()):
            item = QStandardItem(str(i))
            for col, c in enumerate(i.items()):
                child = QStandardItem(str(c))
                item.setChild(col, child)
            if isinstance(model, Domains): item.setEnabled(False)
            self.setItem(row, item)

    def addItem(self, item: Template | Domain):
        self.model.addItem(item)
        sitem = QStandardItem(item.item())
        for i, c in enumerate(item.items()):
            child = QStandardItem(c.item())
            sitem.setChild(i, child)
        self.setItem(self.model.rowCount()-1, sitem)
        if isinstance(self.model, Domains): sitem.setEnabled(False)
        self.layoutChanged.emit()

    def addItems(self, items: List[Domain | Template]):
        self.model.addItems(items)
        self.layoutChanged.emit()

    def addChild(self, index: QModelIndex, item):
        
        if not (index.isValid() or 0 <= index.parent().row() <= self.model.rowCount()):
            return None
        
        self.model.addChild(index.parent().row(), item)
        self.layoutChanged.emit()

    def addChildren(self, index: QModelIndex, items: List[Domain | Template]):

        if not (index.isValid() or 0 <= index.parent().row() <= self.model.rowCount()):
            return None
       
        self.model.addChildren(index.parent().row(), items)
        for i, c in enumerate(self.model.children(index.row())):
            child = QStandardItem(str(c))
            self.item(index.row()).setChild(i, child)

        self.layoutChanged.emit()

    def delChild(self, index: QModelIndex):

        if not index.isValid():
            return None
        
        if not 0 <= (row := index.parent().row()) <= self.model.rowCount():
            return None
        
        if not 0 <= (col := index.row()) <= self.model.columnCount(row):
            return None
        
        self.model.delChild(row, col)
        self.removeRow(col, index.parent())
        self.layoutChanged.emit()

    def delItem(self, index: QModelIndex):

        if not (index.isValid() or 0 <= index.row() <= self.model.rowCount()):
            return None

        self.model.delItem(index.row())
        self.removeRow(index.row())
        self.layoutChanged.emit()

    def parentItem(self, index: QModelIndex) -> Domain:

        if not index.isValid():
            return None
        if 0 <= (row := index.parent().row()) <= self.model.rowCount():
            return None

        return self.model.item(row)

    def childItem(self, index: QModelIndex) -> Boundary | str:

        if not index.isValid():
            return None
        if not 0 <= (row := index.parent().row()) <= self.model.rowCount():
            return None
        if not 0 <= (col := index.row()) <= self.model.columnCount(row):
            return None
        
        return self.model.child(row, col)


    def children(self, index: QModelIndex) -> List[Boundary] | List[str]:
        
        if not index.isValid():
            return None
        if not 0 <= (row := index.parent().row()) <= self.model.rowCount():
            return None
        
        return self.model.children(row)
