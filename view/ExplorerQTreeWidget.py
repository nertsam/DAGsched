import os
from PyQt5.QtWidgets import QTreeWidget


class ExplorerQTreeWidget(QTreeWidget):
    def __init__(self):
        super(QTreeWidget, self).__init__()
        self.path = ''

    def listItems(self, tree):
        for item in os.listdir(self.path):
            path_information = self.path
            path_item =


        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon('assets/folder.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))

