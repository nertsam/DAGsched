from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import networkx as nx

class GraphDrawingQWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        G = nx.DiGraph()

        # add 5 nodes, labeled 0-4:
        map(G.add_node, range(5))
        # 1,2 depend on 0:
        G.add_edge(0, 1)
        G.add_edge(0, 2)
        # 3 depends on 1,2
        G.add_edge(1, 3)
        G.add_edge(2, 3)
        # 4 depends on 1
        G.add_edge(1, 4)

        # now draw the graph:
        pos = {0: (0, 0), 1: (1, 1), 2: (-1, 1),
               3: (0, 2), 4: (2, 2)}
        nx.draw(G, pos, edge_color='r')

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

            # discards the old graph
            # ax.hold(False) # deprecated, see above

            # plot data
        ax.grid()
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
