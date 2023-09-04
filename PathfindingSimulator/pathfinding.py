from node import Node

# Handles pathfinding algorithms (only A* currently)
class Pathfinder():

    openSet = []
    closedSet = []
    path = []

    def __init__(self):
        pass

    # Goes through A* pathfinding algorithm to find the shortest path from one point to another, avoiding any obstacles and staying inside the grid
    def FindPath(mainWindow):     

        Pathfinder.ClearPath()
   
        Pathfinder.openSet.clear()
        Pathfinder.closedSet.clear()
        Pathfinder.path.clear()

        openSetColour = 'green'
        closedSetColour = 'red'
        startNode = None
        endNode = None

        # Find which nodes in node list are start and end node
        for node in mainWindow.nodes:
            if(node.isStart):
                startNode = node
            if(node.isEnd):
                endNode = node

        if (endNode.walkable):
            Pathfinder.openSet.append(startNode)
            
            while len(Pathfinder.openSet) > 0:
                currentNode = Pathfinder.FindLowestFCostNode()
                Pathfinder.openSet.remove(currentNode)

                Pathfinder.closedSet.append(currentNode)

                if currentNode == endNode:
                    if mainWindow.showProgress:
                        for openSetNode in Pathfinder.openSet:
                            openSetNode.SetColour(openSetColour)
                        for closedSetNode in Pathfinder.closedSet:
                            closedSetNode.SetColour(closedSetColour)

                    Pathfinder.RetracePath(startNode, endNode)
                    break

                for neighbourNode in Pathfinder.FindNeighbours(mainWindow, currentNode):
                    if not neighbourNode.walkable or Pathfinder.CheckIfNodeInSet(neighbourNode, Pathfinder.closedSet):
                        continue

                    newMovementCostToNeighbour = currentNode.gCost + Pathfinder.GetDistanceBetweenNodes(currentNode, neighbourNode)

                    if newMovementCostToNeighbour < neighbourNode.gCost or (Pathfinder.CheckIfNodeInSet(neighbourNode, Pathfinder.openSet) == False):
                        neighbourNode.gCost = newMovementCostToNeighbour
                        neighbourNode.hCost = Pathfinder.GetDistanceBetweenNodes(neighbourNode, endNode)
                        neighbourNode.fCost = neighbourNode.gCost + neighbourNode.hCost
                        neighbourNode.parentNode = currentNode

                        if neighbourNode not in Pathfinder.openSet:
                            Pathfinder.openSet.append(neighbourNode)
                        else:
                            for node in Pathfinder.openSet:
                                if node == neighbourNode:
                                    node.gCost = neighbourNode.gCost
                                    node.hCost = neighbourNode.hCost
                                    node.fCost = neighbourNode.fCost
                                    node.parentNode = neighbourNode.parentNode

        print(len(Pathfinder.path))

    # Loops through all nodes in open set and returns node with the lowest F cost to be next currentNode
    # If two nodes have the same F score, compare h cost to find one closest to end node (heuristic)
    def FindLowestFCostNode():
        lowestFCost = Pathfinder.openSet[0]

        for node in Pathfinder.openSet:
            if node.fCost < lowestFCost.fCost:
                lowestFCost = node
            elif node.fCost == lowestFCost.fCost:
                if node.hCost < lowestFCost.hCost:
                    lowestFCost = node

        return lowestFCost

    # Given the current node, find all valid nodes (not obstacles and still within grid) and returns a list containing them so that the algorithm may know which nodes to check next
    def FindNeighbours(mainWindow, currentNode):
        neighbours = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                checkXPos = currentNode.x + x
                checkYPos = currentNode.y + y

                # Iterators through list and returns next neighbourNode that fulfils requirements (correct x and y positions)
                for node in mainWindow.nodes:
                    if node.x == checkXPos and node.y == checkYPos:
                        currentNeighbourNode = node 

                # Check to see if neighbour node is actually inside grid
                if checkXPos >= 0 and checkXPos < mainWindow.gridSize and checkYPos >= 0 and checkYPos < mainWindow.gridSize:
                    # Check to see if node is walkable
                    if currentNeighbourNode.walkable:
                        neighbours.append(currentNeighbourNode)

        return neighbours

    # Attempts to find the given node within the given set returning True if it is found and False if it is not found
    def CheckIfNodeInSet(node, set):
        for n in set:
            if n == node:
                return True
        return False

    # Calculates the distance between two nodes to find g and h costs for nodes in the grid as theyre checked
    def GetDistanceBetweenNodes(nodeA, nodeB):
        distanceX = abs(nodeA.x - nodeB.x)
        distanceY = abs(nodeA.y - nodeB.y)

        if distanceX > distanceY:
            return 14 * distanceY + 10 * (distanceX - distanceY)
        
        return 14 * distanceX + 10 * (distanceY - distanceX)

    # Once the algorithm reaches the desired end point (if it does), this is called to trace back through each nodes parent node (starting from the end node) 
    # to find the optimal path taken during the algorithms previous processing
    def RetracePath(startNode, endNode):
        pathColour = 'pink'

        currentNode = endNode
        while currentNode != startNode:
            currentNode.SetColour(pathColour)
            currentNode = currentNode.parentNode

        startNode.SetColour(pathColour)

    # Loops through open/closed and path sets, setting any node that is not the start node, within these sets, to its default values/colour 
    # so that the user may alter the environment for a new path
    def ClearPath():
        if len(Pathfinder.closedSet) > 0 and len(Pathfinder.openSet) > 0:
            for node in (Pathfinder.closedSet + Pathfinder.openSet):
                if node.isStart:
                    node.SetColour(Node.startColour)
                elif node.isEnd:
                    node.SetColour(Node.endColour)
                elif node.isObstacle:
                    pass
                else:
                    node.SetDefault()

        if len(Pathfinder.path) > 0:
            for pathNode in Pathfinder.path:
                if pathNode.isStart == False and pathNode.isEnd == False:
                    pathNode.SetDefault()
