from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox,
    QErrorMessage
)


from tools.tools import generate_dialog


class Dialog(QDialog):

    def __init__(self, title: str, objects: dict, model=None, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, f)

        self.objects = [obj['name'] for obj in objects]

        layout = QVBoxLayout()
        self.data = {}

        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle(title)
        
        btn = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)

        layout.addLayout(generate_dialog(objects, model))
        layout.addWidget(btn)
        self.setLayout(layout)

    def accept(self):
        for child in self.children():
            if (name := child.objectName()) in self.objects:
                try:
                    self.data[name] = child.data()
                except ValueError:
                    msg = QErrorMessage()
                    msg.setWindowTitle('Value error')
                    msg.showMessage(f'There must be no empty fields in the form.')
                    msg.exec()
                    return None
        return super().accept()
    
    def reject(self):
        self.data = None
        return super().reject()
