from graph import Node
from graph import Position
from globalconsts import *
import sys
global FLOOR
class AStar:
	def __init__(self, gameMap):
		self.gameMap = gameMap;
		self.visitedPositions = [];
		self.stack = [];

	def findMinimum(self):
		n = self.stack[0]
		minId = 0
		for i in xrange(0, len(self.stack)):
			if(self.stack[i].cost < self.stack[minId].cost):
				minId = i
		new = self.stack.pop(minId)
		return new

	def solveBetweenNodes(self, clusterIds, nodeA, goal):
		self.visitedPositions = [];
		cost = self.calculateHeuristic(nodeA.position, goal.position)
		start = Node(nodeA.position, nodeA.clusterId, cost);
		self.stack = [start];
		while len(self.stack) > 0:
			# Find minimum active node
			currentNode = self.findMinimum()
			if currentNode.position == goal.position:
				return cost
			self.calculateHeuristic(currentNode.position, goal.position)
			self.addNeighbouringNodes(currentNode, goal, clusterIds)

			self.setVisited(currentNode.position)

		return -1

	def setVisited(self, position):
		self.visitedPositions.append(position)

	def isVisited(self, position):
		for n in self.visitedPositions:
			if(position.x == n.x and position.y == n.y):
				return True;
		return False;

	def addNeighbouringNodes(self, node, goal, clusterIds):
		pos = node.position;
		posArr = [Position(pos.x + 1, pos.y),
		Position(pos.x, pos.y + 1),
		Position(pos.x - 1, pos.y),
		Position(pos.x, pos.y - 1)];
		for p in posArr:
			if (self.gameMap.isPositionValid(p)):
				if self.gameMap[p.x, p.y] == WALL:
					self.setVisited(p)

			if self.gameMap.isPositionValid(p) and not self.isVisited(p):
				cid = self.gameMap.convertMapv2ClusterId(p);

				if(cid in clusterIds):
					cost = self.calculateHeuristic(p, goal.position)
					n = Node(p, cid, cost)
					self.stack.append(n)

			else:
				self.setVisited(p)

	# Manhattan distance between nodes
	def calculateHeuristic(self, nodePos, goalPos):
		x = nodePos.x - goalPos.x;
		y = nodePos.y - goalPos.y;
		return abs(x) + abs(y);


