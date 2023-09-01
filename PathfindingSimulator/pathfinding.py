
def FindPath(mainWindow):
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
                                                                    # TODO: AFTER PATH HAS BEEN FOUND, LOOP THROUGH OPEN, CLOSED AND PATH LISTS AND SET NODE COLOURS ACCORDINGLY
    if (endNode.walkable):
        openSet = []
        closedSet = []
        openSet.append(startNode)
        
        while len(openSet) > 0:
            currentNode = FindLowestFCostNode(openSet)
            openSet.remove(currentNode)

            closedSet.append(currentNode)

            if currentNode == endNode:
                if mainWindow.showProgress:
                    for openSetNode in openSet:
                        openSetNode.SetColour(openSetColour)
                    for closedSetNode in closedSet:
                        closedSetNode.SetColour(closedSetColour)

                RetracePath(startNode, endNode)
                break

            for neighbourNode in FindNeighbours(mainWindow, currentNode):
                if not neighbourNode.walkable or CheckIfNodeInSet(neighbourNode, closedSet):
                    continue

                newMovementCostToNeighbour = currentNode.gCost + GetDistanceBetweenNodes(currentNode, neighbourNode)

                if newMovementCostToNeighbour < neighbourNode.gCost or (CheckIfNodeInSet(neighbourNode, openSet) == False):
                    neighbourNode.gCost = newMovementCostToNeighbour
                    neighbourNode.hCost = GetDistanceBetweenNodes(neighbourNode, endNode)
                    neighbourNode.fCost = neighbourNode.gCost + neighbourNode.hCost
                    neighbourNode.parentNode = currentNode

                    if neighbourNode not in openSet:
                        openSet.append(neighbourNode)
                    else:
                        for node in openSet:
                            if node == neighbourNode:
                                node.gCost = neighbourNode.gCost
                                node.hCost = neighbourNode.hCost
                                node.fCost = neighbourNode.fCost
                                node.parentNode = neighbourNode.parentNode



# Loops through all nodes in open set and returns node with the lowest F cost to be next currentNode
def FindLowestFCostNode(openSet):
    lowestFCost = openSet[0]

    for node in openSet:
        if node.fCost < lowestFCost.fCost:
            lowestFCost = node
        elif node.fCost == lowestFCost.fCost:
            if node.hCost < lowestFCost.hCost:
                lowestFCost = node

    return lowestFCost

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

def CheckIfNodeInSet(node, set):
    for n in set:
        if n == node:
            return True
    return False

def GetDistanceBetweenNodes(nodeA, nodeB):
    distanceX = abs(nodeA.x - nodeB.x)
    distanceY = abs(nodeA.y - nodeB.y)

    if distanceX > distanceY:
        return 14 * distanceY + 10 * (distanceX - distanceY)
    
    return 14 * distanceX + 10 * (distanceY - distanceX)

def RetracePath(startNode, endNode):
    path = []
    pathColour = 'pink'

    currentNode = endNode
    while currentNode != startNode:
        path.append(currentNode)
        currentNode = currentNode.parentNode

    path.append(startNode)

    for node in path:
        node.SetColour(pathColour)