from graph import Node
from graph import Position
from globalconsts import *
from path import Path

global FLOOR
class AStar:
    def __init__(self, gameMap):
        self.gameMap = gameMap
        self.visitedPositions = []
        self.stack = []

    def findMinimum(self):
        minId = 0
        for i in range(0, len(self.stack)):
            if self.stack[i].cost < self.stack[minId].cost:
                minId = i
        new = self.stack.pop(minId)
        return new

    def solveBetweenNodes(self, clusterIds, nodeA, goal):
        check = False
        # Make sure that nodes belongs to same player
        for sId in nodeA.affectedPlayers:
            for gId in goal.affectedPlayers:
                if gId is ALL_PLAYERS or sId is ALL_PLAYERS or sId is gId:
                    check = True

        if check:
            self.visitedPositions = []
            cost = self.calculateHeuristic(nodeA, goal, None)
            start = Node(nodeA.position, nodeA.clusterId, nodeA.affectedPlayers, cost, 0)
            self.stack = [start]
            while len(self.stack) > 0:
                # Find minimum active node
                currentNode = self.findMinimum()
                if currentNode.position == goal.position:
                    # Create list of nodes from start to goal

                    return self.getReturn(currentNode)

                self.addNeighbouringNodes(currentNode, goal, clusterIds)

                self.setVisited(currentNode.position)
        return -1

    def getReturn(self, node):
        return node.length

    def setVisited(self, position):
        self.visitedPositions.append(position)

    def isVisited(self, position):
        for n in self.visitedPositions:
            if position.x == n.x and position.y == n.y:
                return True
        return False

    def addNeighbouringNodes(self, node, goal, clusterIds):
        pos = node.position
        posArr = [Position(pos.x + 1, pos.y),
                  Position(pos.x, pos.y + 1),
                  Position(pos.x - 1, pos.y),
                  Position(pos.x, pos.y - 1)]
        for p in posArr:
            if self.gameMap.isPositionValid(p):
                if self.gameMap[p.x, p.y] == WALL:
                    self.setVisited(p)

            if self.gameMap.isPositionValid(p) and not self.isVisited(p):
                cid = self.gameMap.convertMapv2ClusterId(p)

                if cid in clusterIds or ALL_CLUSTERS in clusterIds:
                    n = Node(p, cid, node.affectedPlayers, 0, node.length + 1, node)
                    n.cost = self.calculateHeuristic(n, goal, node.parent)
                    self.stack.append(n)
            else:
                self.setVisited(p)

        # Manhattan distance between nodes
    def calculateHeuristic(self, node, goal, parent = None):
        nodePos = node.position
        goalPos = node.position
        x = nodePos.x - goalPos.x
        y = nodePos.y - goalPos.y
        return abs(x) + abs(y)

class PathAStar(AStar):
    def getReturn(self, node):
        return node

class GraphAStar(AStar):
    def __init__(self, gameMap):
        AStar.__init__(self, gameMap)
        self.mapSolver = PathAStar(gameMap)

    def calculateHeuristic(self, node, goal, parent = None):
        if parent is None:
            return 0
        for edge in self.gameMap.edges:
            if ((edge.i1.position == node.position and edge.i2.position == parent.position) or
                    (edge.i2.position == node.position and edge.i1.position == parent.position)):
                return parent.cost + edge.cost

    def getReturn(self, currentNode):
        path = Path()
        nodes = []
        self.iterateAddNode(currentNode, nodes)
        for i in range(len(nodes) - 1):
            self.iterativeGetReturn(nodes[i], nodes[i + 1], path)
        return path

    def iterateAddNode(self, node, nodes):
        if node != None:
            nodes.append(node)
            self.iterateAddNode(node.parent, nodes)

    def iterateAddToPath(self, node, path, goalPosition):
        if node != None:
            if node.position != goalPosition:
                path.addPosition(node.position)
                self.iterateAddToPath(node.parent, path, goalPosition)

    def iterativeGetReturn(self, node, node2, path):
        n = self.mapSolver.solveBetweenNodes([ALL_CLUSTERS], node, node2)
        if n != -1:
            # self.iterativeGetReturn(n, path, node.parent.position)
            self.iterateAddToPath(n, path, node2.position)


    def addNeighbouringNodes(self, parent, goal, clusterIds):
        for edge in self.gameMap.graph.edges:
            node = None
            if edge.i1.position == parent.position:
                if not self.isVisited(edge.i2.position):
                    node = edge.i2

            elif edge.i2.position == parent.position:
                if not self.isVisited(edge.i1.position):
                    node = edge.i1

            # This comes true when we have a valid new node.
            if node is not None:
                n = Node(node.position, node.clusterId, node.affectedPlayers, parent.cost + edge.cost, parent.length + edge.cost, parent)
                self.stack.append(n)
