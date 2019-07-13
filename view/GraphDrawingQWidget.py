from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import networkx as nx


class GraphDrawingQWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graph = nx.DiGraph()

        # add 5 nodes, labeled 0-4:
        map(self.graph.add_node, range(5))
        # 1,2 depend on 0:
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        # 3 depends on 1,2
        self.graph.add_edge(1, 3)
        self.graph.add_edge(2, 3)
        # 4 depends on 1
        self.graph.add_edge(1, 4)

        # now draw the graph:
        pos = {0: (0, 0), 1: (1, 1), 2: (-1, 1),
               3: (0, 2), 4: (2, 2)}

        nx.draw(self.graph, pos, edge_color='b')

        self.canvas.draw()

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
