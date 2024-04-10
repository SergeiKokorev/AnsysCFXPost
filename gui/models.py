from dataclasses import dataclass, field
from typing import Any, List
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


from models.data import Template


class TemplateModel(QAbstractListModel):

    def __init__(self, *args, templates=None, **kwargs):

        super(TemplateModel, self).__init__(*args, **kwargs)
        self.templates = templates or []

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        
        if not index.isValid():
            return None
        
        if not 0 <= index.row() <= self.rowCount():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            name = self.templates[index.row()].name
            return name
        
    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.templates)

    def item(self, index: QModelIndex) -> Template:
        if not index.isValid():
            return None
        if not 0 <= index.row() <= self.rowCount():
            return None
        return self.templates[index.row()]
