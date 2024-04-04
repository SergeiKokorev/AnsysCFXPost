from typing import Any, Dict, List
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


from models.data import Domain, Boundary


class ListModel(QAbstractListModel):

    def __init__(self, *args, model: List[Domain], **kwargs) -> None:
        super(ListModel, self).__init__(*args, **kwargs)

        self.model = [i for dmn in model for i in dmn.children]

    def rowCount(self, parent: QModelIndex=None) -> int:
        return len(self.model)
    
    def columnCount(self, parent: QModelIndex=None) -> int:
        return 1
    
    def data(self, index: QModelIndex, role: int = ...) -> Any:
        
        if not index.isValid():
            return None
        
        if not 0 <= index.row() <= self.rowCount():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.model[index.row()])


class TreeModel(QStandardItemModel):
    
    def __init__(self, *args, model: List[Domain], **kwargs):
        super(TreeModel, self).__init__(*args, **kwargs)

        self.model = model

        for row, i in enumerate(self.model):
            item = QStandardItem(str(i))
            item.setSelectable(False)
            for col, c in enumerate(i.children):
                child = QStandardItem(str(c))
                item.setChild(col, child)

            self.setItem(row, item)

    def parentItem(self, index: QModelIndex) -> Domain:

        if not index.isValid():
            return None
        
        row = index.parent().row()
        if not 0 <= row <= len(self.model):
            return None
        
        return self.model[row]

    def childItem(self, index: QModelIndex) -> Boundary:

        if not (parent := self.parentItem(index)):
            return None
        if not 0 <= (column := index.row()) <= parent.childCount():
            return None
        
        return parent.child(column)
            

    def children(self, index: QModelIndex) -> List[Boundary]:
        if (item := self.parentItem(index)):
            return item.children
        else:
            return None
