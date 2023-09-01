from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QComboBox, QCheckBox, QRadioButton, QPushButton
from PySide6.QtCore import Qt, QPoint
from enum import Enum

from colour import Colour
from node import Node, User
from pathfinding import FindPath

class MainWindow(QMainWindow):

    nodes = []
    gridSize = 20

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Simulator")
        self.setFixedSize(640, 480)

        self.user = User()
        #self.user.show()
        
        self.SetupOptionWidgets()

        self.SetupNodeGrid()                                                        # Creates node grid base widget and QGridLayout to store nodes in

        # Adding newly setup option (left) and node grid (right) layouts (inside their respective widgets) to the windows "base" layout
        baseLayout = QHBoxLayout(self)
        baseLayout.addWidget(self.optionsWidget, 1)
        baseLayout.addWidget(self.gridWidget, 9)
        
        mainWidget = QWidget()
        mainWidget.setLayout(baseLayout)

        self.setCentralWidget(mainWidget)

    def SetNodeToPlace(self, user, nodeState):
        user.nodeToPlace = user.NodeToPlace[nodeState]

    # Functionality to create and organise widgets in left (settings/options) section   
    def SetupOptionWidgets(self):
        self.optionsWidget = QWidget()
        self.options = QVBoxLayout(self.optionsWidget)

        self.optionsTitle = QLabel("Pathfinding: ")
        self.algorithmSubtitle = QLabel("Algorithm: ")

        class Algorithms(Enum):
            AStar = 1

        self.algorithmOptions = QComboBox()
        for algorithm in Algorithms:
            self.algorithmOptions.addItem(algorithm.name)

        # Show progress checkbox
        self.showProgress = True
        self.showProgressBox = QCheckBox("Show Progress")
        self.showProgressBox.setChecked(True)
        self.showProgressBox.clicked.connect(lambda: self.SetShowProgress())

        self.AddNodePalette()

        self.startAlgorithm = QPushButton("Start")
        self.startAlgorithm.clicked.connect(lambda: FindPath(self))
        self.clearGrid = QPushButton("Clear")
        self.clearGrid.clicked.connect(lambda: self.ClearNodeGrid())
        
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttonsWidget)

        self.buttonsLayout.addWidget(self.startAlgorithm)
        self.buttonsLayout.addWidget(self.clearGrid)
        self.buttonsLayout.setSpacing(0.5)

        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.AddWidgetsToOptionsLayout()

    def SetShowProgress(self):
        self.showProgress = self.showProgressBox.isChecked()


    # Create and add functionality to node palette radio buttons
    def AddNodePalette(self):
        self.nodePalette = QLabel("Palette: ")

        self.startColour = Colour(Node.startColour)
        self.startCheck = QRadioButton("Start ")
        self.startCheck.setChecked(True)
        self.startCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "Start"))

        self.endColour = Colour(Node.endColour)
        self.endCheck = QRadioButton("End ")
        self.endCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "End"))

        self.obstacleColour = Colour(Node.obstacleColour)
        self.obstacleCheck = QRadioButton("Obstacle ")
        self.obstacleCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "Obstacle"))

    # Adds all relevant created widgets to vertical box layout (options) on the left side of the application
    def AddWidgetsToOptionsLayout(self):
        self.paletteGrid = QGridLayout(self)
        self.paletteGrid.addWidget(self.startColour, 0, 0, 2, 1)                                # (widgetToAdd, rowNum, columnNum, rowsToSpan,columnsToSpan
        self.paletteGrid.addWidget(self.startCheck, 0, 1, 1, 3)
        self.paletteGrid.addWidget(self.endColour, 1, 0, 2, 1)
        self.paletteGrid.addWidget(self.endCheck, 1, 1, 1, 3)
        self.paletteGrid.addWidget(self.obstacleColour, 2, 0, 2, 1)
        self.paletteGrid.addWidget(self.obstacleCheck, 2, 1, 1, 3)
        
        self.paletteWidget = QWidget()
        self.paletteWidget.setLayout(self.paletteGrid)

        self.options.addWidget(self.optionsTitle, 1.5, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.algorithmSubtitle, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.algorithmOptions, 1.5, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.showProgressBox, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.nodePalette, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.paletteWidget, 1.5, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.buttonsWidget, alignment=Qt.AlignmentFlag.AlignTop)

    # Creates specified nodes and adds them to a QGridLayout for organisation
    def SetupNodeGrid(self):
        # Node Grid:
        for i in range(MainWindow.gridSize):
            for j in range(MainWindow.gridSize):
                MainWindow.nodes.append(Node(j, i, True, False, False, False, self.user))

        self.gridWidget = QWidget()

        self.nodeGrid = QGridLayout(self.gridWidget)

        for node in MainWindow.nodes:
            self.nodeGrid.addWidget(node, node.y, node.x)

        self.nodeGrid.setSpacing(1)

    def ClearNodeGrid(self):
        if self.nodeGrid.count() > 0:
            for i in range(self.nodeGrid.count()):
                currentNode = self.nodeGrid.itemAt(i).widget()
                currentNode.SetDefault()
            Node.ResetNodeValues()
            