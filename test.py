import os
from PySide6.QtWidgets import (
    QVBoxLayout, QApplication, QMainWindow,
    QListView, QTreeView, QComboBox, QWidget,
    QPushButton, QLabel
)
from PySide6.QtCore import QModelIndex

from models.data import *
from models.gui import *
from gui.dialogues import TemplateDialog
from tools.tools import get_data


FILE = os.path.join('test_data', 'result.out')
FILES = ['f1.res', 'f2.res', 'f3.res']


def main():
    
    tmp1 = Template(name='Axial1', data={'inlet': ('Inlet', 'Hub')})
    tmp2 = Template(name='Axial2', data={'outlet': ('Outlet', 'Hub')})


    domains, boundaries = get_data(FILE)
    templates = Templates()
    templates.addItems([tmp1, tmp2])    

    app = QApplication()
    window = QMainWindow()

    listModel = ListModel(model=boundaries)
    treeModel = TreeModel(model=domains)
    tmpTreeModel = TreeModel(model=templates)
    layout = QVBoxLayout()
    central_widget = QWidget()

    listView = QListView()
    listView.setModel(listModel)

    treeView = QTreeView()
    treeView.setHeaderHidden(True)
    treeView.setModel(treeModel)

    tmpTreeView = QTreeView()
    tmpTreeView.setModel(tmpTreeModel)
    tmpTreeView.setHeaderHidden(True)

    cmbView = QComboBox()
    cmbView.setModel(listModel)

    btn1 = QPushButton('Add files')
    btn1.clicked.connect(lambda: add_files(tmpTreeView, tmpTreeModel))
    btn2 = QPushButton('Del file')
    btn2.clicked.connect(lambda: del_file(tmpTreeView, tmpTreeModel))
    btn3 = QPushButton('Del Temp')
    btn3.clicked.connect(lambda: del_tmp(tmpTreeView, tmpTreeModel))

    layout.addWidget(listView)
    layout.addWidget(treeView)
    layout.addWidget(tmpTreeView)
    layout.addWidget(cmbView)
    layout.addWidget(btn1)
    layout.addWidget(btn2)
    layout.addWidget(btn3)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.show()
    app.exec()



def add_files(tree_view: QTreeView, tree_model: TreeModel):
    index = tree_view.currentIndex()
    tree_model.addChildren(index, FILES)


def del_file(tree_view: QTreeView, tree_model: TreeModel):
    index = tree_view.currentIndex()
    tree_model.delChild(index)


def del_tmp(tree_view: QTreeView, tree_model: TreeModel):
    index = tree_view.currentIndex()
    tree_model.delItem(index)


if __name__ == "__main__":
    main()
