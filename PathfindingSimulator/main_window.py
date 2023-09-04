from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QComboBox, QCheckBox, QRadioButton, QPushButton
from PySide6.QtCore import Qt, QPoint
from enum import Enum

from colour import Colour
from node import Node, User
from pathfinding import Pathfinder

class MainWindow(QMainWindow):

    nodes = []
    gridSize = 20
    baseWindowTitle = "Pathfinding Simulator"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(MainWindow.baseWindowTitle)
        self.setFixedSize(640, 480)

        self.user = User()
        
        self.SetupOptionWidgets()

        self.SetupNodeGrid()                                                        # Creates node grid base widget and QGridLayout to store nodes in

        # Adding newly setup option (left) and node grid (right) layouts (inside their respective widgets) to the windows "base" layout
        baseLayout = QHBoxLayout()
        baseLayout.addWidget(self.optionsWidget, 1)
        baseLayout.addWidget(self.gridWidget, 9)
        
        mainWidget = QWidget()
        mainWidget.setLayout(baseLayout)

        self.setCentralWidget(mainWidget)

    # Changes value of a bool which determines what type of node the user will place (Start/End/Obstacle) given through the nodeState parameter, this will be called by each radiobutton
    def SetNodeToPlace(self, user, nodeState):
        user.nodeToPlace = user.NodeToPlace[nodeState]

    # Functionality to create and organise widgets in left (settings/options) section   
    def SetupOptionWidgets(self):
        self.optionsWidget = QWidget()
        self.options = QVBoxLayout(self.optionsWidget)

        titleFont = self.font()
        titleFont.setPointSize(20)
        self.subtitleFont = self.font()
        self.subtitleFont.setPointSize(12)

        self.optionsTitle = QLabel("Pathfinding: ")
        self.optionsTitle.setFont(titleFont)
        self.algorithmSubtitle = QLabel("Algorithm: ")
        self.algorithmSubtitle.setFont(self.subtitleFont)

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
        self.startAlgorithm.clicked.connect(lambda: Pathfinder.FindPath(self))
        self.resetPath = QPushButton("Clear Path")
        self.resetPath.clicked.connect(lambda: Pathfinder.ClearPath())
        self.clearGrid = QPushButton("Clear All")
        self.clearGrid.clicked.connect(lambda: self.ClearNodeGrid())
        
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QGridLayout(self.buttonsWidget)

        self.buttonsLayout.addWidget(self.startAlgorithm, 0, 0)
        self.buttonsLayout.addWidget(self.clearGrid, 1, 0)
        self.buttonsLayout.addWidget(self.resetPath, 0, 1)
        self.buttonsLayout.setSpacing(0.5)

        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.AddWidgetsToOptionsLayout()

    # Sets showProgress bool to value of the UI checkbox
    def SetShowProgress(self):
        self.showProgress = self.showProgressBox.isChecked()


    # Create and add functionality to node palette radio buttons
    def AddNodePalette(self):
        self.nodePalette = QLabel("Palette: ")
        self.nodePalette.setFont(self.subtitleFont)

        self.startColour = Colour(Node.startColour)
        self.startCheck = QRadioButton("Start")
        self.startCheck.setChecked(True)
        self.startCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "Start"))

        self.endColour = Colour(Node.endColour)
        self.endCheck = QRadioButton("End")
        self.endCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "End"))

        self.obstacleColour = Colour(Node.obstacleColour)
        self.obstacleCheck = QRadioButton("Obstacle")
        self.obstacleCheck.clicked.connect(lambda: self.SetNodeToPlace(self.user, "Obstacle"))

    # Adds all relevant created widgets to vertical box layout (options) on the left side of the application
    def AddWidgetsToOptionsLayout(self):
        self.paletteGrid = QGridLayout()
        self.paletteGrid.addWidget(self.startColour, 0, 0, 2, 1)                                            # (widgetToAdd, rowNum, columnNum, rowsToSpan ,columnsToSpan)
        self.paletteGrid.addWidget(self.startCheck, 0, 1, 1, 3)
        self.paletteGrid.addWidget(self.endColour, 1, 0, 2, 1)
        self.paletteGrid.addWidget(self.endCheck, 1, 1, 1, 3)
        self.paletteGrid.addWidget(self.obstacleColour, 2, 0, 2, 1)
        self.paletteGrid.addWidget(self.obstacleCheck, 2, 1, 1, 3)
        
        self.paletteWidget = QWidget()
        self.paletteWidget.setLayout(self.paletteGrid)

        self.options.addWidget(self.optionsTitle, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.algorithmSubtitle, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.algorithmOptions, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.showProgressBox, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.nodePalette, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.paletteWidget, alignment=Qt.AlignmentFlag.AlignTop)
        self.options.addWidget(self.buttonsWidget, 5, alignment=Qt.AlignmentFlag.AlignTop)

    # Creates specified nodes and adds them to a QGridLayout for organisation
    # Acts as the canvas for the user to draw their environment and simulate pathfinding
    def SetupNodeGrid(self):
        # Node Grid:
        for i in range(MainWindow.gridSize):
            for j in range(MainWindow.gridSize):
                MainWindow.nodes.append(Node(j, i, True, False, False, False, self.user))

        self.gridBgndColour = 'black'
        self.gridWidget = Colour(self.gridBgndColour)

        self.nodeGrid = QGridLayout(self.gridWidget)

        for node in MainWindow.nodes:
            self.nodeGrid.addWidget(node, node.y, node.x)

        self.nodeGrid.setSpacing(1)

    # Comepletely clear the node grid and set all the node values back to their default state giving the user the option to start from scratch
    def ClearNodeGrid(self):
        if self.nodeGrid.count() > 0:
            for i in range(self.nodeGrid.count()):
                currentNode = self.nodeGrid.itemAt(i).widget()
                currentNode.SetDefault()
            Node.ResetNodeCountValues()
            