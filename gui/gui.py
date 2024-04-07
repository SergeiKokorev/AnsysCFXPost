from copy import deepcopy
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox,
    QErrorMessage
)


from tools.tools import generate_dialog
from gui.models import Template
from tools.const import MVC_WIDGETS as mvc, WIDGETS as wg


class Dialog(QDialog):

    def __init__(self, title: str, objects: list, model, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, f)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        self.objects = deepcopy(objects)
        self.template = None
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

    def accept(self):

        tmp_data = dict([(w['name'], None) for w in self.objects])
        self.template = Template(name=self.title, data=tmp_data)
        widgets = {**mvc, **wg}

        for widget in self.objects:
            child = self.findChild(widgets[widget['widget']], widget['name'])
            if child: self.template.data[widget['name']] = ( widget['title'], child.data())

        return super().accept()
    
    def reject(self):
        self.template = None
        return super().reject()
