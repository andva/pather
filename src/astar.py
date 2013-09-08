from graph import Node
from graph import Position
from globalconsts import *

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
            cost = self.calculateHeuristic(nodeA.position, goal.position)
            start = Node(nodeA.position, nodeA.clusterId, nodeA.affectedPlayers, cost, 0)
            self.stack = [start]
            while len(self.stack) > 0:
                # Find minimum active node
                currentNode = self.findMinimum()
                if currentNode.position == goal.position:
                    return currentNode.length
                self.calculateHeuristic(currentNode.position, goal.position)
                self.addNeighbouringNodes(currentNode, goal, clusterIds)

                self.setVisited(currentNode.position)

        return -1

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

                if cid in clusterIds:
                    cost = self.calculateHeuristic(p, goal.position)
                    n = Node(p, cid, node.affectedPlayers, cost, node.length + 1)
                    self.stack.append(n)
            else:
                self.setVisited(p)

        # Manhattan distance between nodes
    def calculateHeuristic(self, nodePos, goalPos):
        x = nodePos.x - goalPos.x
        y = nodePos.y - goalPos.y
        return abs(x) + abs(y)

