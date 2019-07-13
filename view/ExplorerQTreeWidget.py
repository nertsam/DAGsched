import os
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class ExplorerQTreeWidget(QTreeWidget):
    def __init__(self):
        super(QTreeWidget, self).__init__()

    @staticmethod
    def enumerateChildren(path, tree):
        for item in os.listdir(path):
            parent = QTreeWidgetItem(QTreeWidget, [os.path.basename(item)])
            if os.path.isdir(path):
                ExplorerQTreeWidget.enumerateChildren(path, parent)


        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon('assets/folder.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))

