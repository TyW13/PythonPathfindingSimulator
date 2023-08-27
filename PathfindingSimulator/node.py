from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QPalette, QColor
from enum import Enum


class User(QWidget):

    class NodeToPlace(Enum):
            Start = 1
            End = 2
            Obstacle = 3

    def __init__(self):
        super(User, self).__init__()

        self.nodeToPlace = User.NodeToPlace.Start

class Node(QWidget):

    startNodeCount = 0
    endNodeCount = 0
    nodeSize = QSize(0, 0)                                                          # Initialising nodeSize var to be changed later

    defaultColour = 'darkGreen'
    startColour = 'cyan'
    endColour = 'magenta'
    obstacleColour = 'black'

    def __init__(self, x, y, walkable, occupied, start, end, user):
        super(Node, self).__init__()
        
        self.setAutoFillBackground(True)
        self.SetColour(Node.defaultColour)

        self.relativePos = QPoint(0, 0)
        self.x = x
        self.y = y
        self.walkable = walkable
        self.occupied = occupied
        self.start = start
        self.end = end

        self.user = user

        self.setMouseTracking(True)

    def SetColour(self, colour):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colour))
        self.setPalette(palette)

    def RemoveNode(self):
        self.walkable = True
        self.occupied = False
        if self.start:
            self.start = False
            Node.startNodeCount -= 1
        elif self.end:
            self.end = False
            Node.endNodeCount -= 1
        self.SetColour(Node.defaultColour)
        
    def SetStart(self):
        if Node.startNodeCount == 0:
            self.start = True
            self.walkable = True
            self.occupied = True
            self.SetColour(QColor(Node.startColour))
            Node.startNodeCount += 1
    
    def SetEnd(self):
        if Node.endNodeCount == 0:
            self.end = True
            self.walkable = True
            self.occupied = True
            self.SetColour(QColor(Node.endColour))
            Node.endNodeCount += 1

    def SetObstacle(self):
        self.walkable = False
        self.occupied = True
        self.SetColour(QColor(Node.obstacleColour))

    # Changes clicked node to appropriate node based on which option the user selected
    def drawCurrentNode(self):
        if(self.user.nodeToPlace == self.user.NodeToPlace.Start):
                self.SetStart()
        elif(self.user.nodeToPlace == self.user.NodeToPlace.End):
                self.SetEnd()
        elif(self.user.nodeToPlace == self.user.NodeToPlace.Obstacle):
                self.SetObstacle()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.occupied == False:
            self.drawCurrentNode()

        elif event.button() == Qt.MouseButton.RightButton and self.occupied == True:
            self.RemoveNode()

    def moveEvent(self, e):
         self.relativePos = self.pos()
    
    def resizeEvent(self, e):
         Node.nodeSize = self.size()

    def sizeHint(self):
         return QSize(100, 100)