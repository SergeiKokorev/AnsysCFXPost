from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox,
    QErrorMessage
)


from tools.tools import generate_dialog


class Dialog(QDialog):

    def __init__(self, title: str, objects: list, model=None, parent: QWidget = None, f: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, f)

        self.objects = objects.copy()

        layout = QVBoxLayout()
        self.data = None

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
        self.data = {}
        objects = [obj['name'] for obj in self.objects]
        for child in self.children():
            if (name := child.objectName()) in objects:
                try:
                    title = [obj['title'] for obj in self.objects if obj['name'] == name][0]
                    self.data[name] = (title, child.data())
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
