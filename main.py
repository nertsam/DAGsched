import sys
import PyQt5.QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, QMenuBar
from view import MouseTrackingQWidget, TaskGeneratorQWidget, TaskStatisticsQWidget, GraphDrawingQWidget

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'DAGsched'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.menuBar = QMenuBar()
        self.menuBar.addMenu('&File')
        self.menuBar.addMenu('&Edit')
        self.menuBar.addMenu('&Settings')
        self.menuBar.addMenu('&View')

        self.setMenuBar(self.menuBar)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(PyQt5.QtGui.QIcon('./res/logo.png'))
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabMouseTracking = MouseTrackingQWidget.MouseTrackingQWidget()
        self.tabTaskGenerator = TaskGeneratorQWidget.TaskGeneratorQWidget()
        self.tabTaskStatistics = TaskStatisticsQWidget.TaskStatisticsQWidget()
        self.tabGraphDrawing = GraphDrawingQWidget.GraphDrawingQWidget()
        self.tabs.resize(300, 200)
        self.tabs.addTab(self.tabMouseTracking, 'Mouse Tracking')
        self.tabs.addTab(self.tabTaskGenerator, 'Task Generator')
        self.tabs.addTab(self.tabTaskStatistics, 'Task Statistics')
        self.tabs.addTab(self.tabGraphDrawing, 'Graphs')
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
