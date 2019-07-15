import sys
import PyQt5.QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, \
    QAction, QMenuBar, QToolBar, QStatusBar
from view import MouseTrackingQWidget, TaskGeneratorQWidget, TaskStatisticsQWidget, GraphDrawingQWidget


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'DAGsched - DAG Generation & Analysis Suite'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600

        self.menuBar = QMenuBar()
        self.menuBar.addMenu('&File')
        self.menuBar.addMenu('&Edit')
        self.menuBar.addMenu('&Settings')
        self.menuBar.addMenu('&View')

        maximizeAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-home-24px.svg'), 'Maximize', self)
        minimizeAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-build-24px.svg'), 'Minimize', self)
        scheduleAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-schedule-24px.svg'), 'Schedule', self)

        createNewFolderAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-create_new_folder-24px.svg'), 'New Folder', self)
        createAnalysisAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-pie_chart-24px.svg'), 'Analysis', self)
        saveAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-save-24px.svg'), 'Save', self)
        simulateScheduleAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-undo-24px.svg'), 'Simulate', self)

        zoomInAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-zoom_in-24px.svg'), 'Zoom In', self)
        zoomOutAction = QAction(PyQt5.QtGui.QIcon('./res/icons/baseline-zoom_out-24px.svg'), 'Zoom Out', self)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.toolBar = self.addToolBar("MainToolBar")

        self.toolBar.addAction(maximizeAction)
        self.toolBar.addAction(minimizeAction)
        self.toolBar.addAction(scheduleAction)
        self.toolBar.addAction(createAnalysisAction)
        self.toolBar.addAction(createNewFolderAction)
        self.toolBar.addAction(saveAction)
        self.toolBar.addAction(zoomInAction)
        self.toolBar.addAction(zoomOutAction)
        self.toolBar.addAction(simulateScheduleAction)


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
