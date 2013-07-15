class AStar:
	def __init__(self, gameMap):
		self.gameMap = gameMap;
		self.visitedPositions = [];
		self.stack = [];
	def findMinimum(self, nodes):
		n = nodes[0];
		for i in range(0, nodes.length()):
			if(nodes[i].cost < n.cost):
				n = nodes[i];
		return n;


	def solveBetweenNodes(self, clusterId, nodeA, goal):
		self.visitedPositions = [];
		start = Node(nodeA.position, nodeA.clusterId, 0);
		self.stack = [start];
		while self.stack.length() > 0:
			# Find minimum active node
			currentNode = self.findMinimum(self.stack);
			addNeighbouringNodes(currentNode,  self.stack);

	def isVisited(self, node):
		for n in self.visitedPositions:
			if(node.position.x == n.x and node.position.y == n.y):
				return True;
		return False;

	def addNeighbouringNodes(self, node, nodeList):
		pos = node.position;
		posArr = [Position(pos.x + 1, pos.y),
		Position(pos.x, pos.y + 1),
		Position(pos.x - 1, pos.y),
		Position(pos.x, pos.y - 1)];
		for p in posArr:
			if(self.gameMap.isValidPosition(p)):
				if( not self.isVisited(p)):
					cid = self.gameMap.convertMapv2ClusterId(p);
					if(cid == node.clusterId):
						nodeList.append(Node(p, cid, node.cost))


	# Manhattan distance between nodes
	def calculateHeuristic(self, node, goal):
		x = node.position.x - goal.position.x;
		y = node.position.y - goal.position.y;

		return abs(x) + abs(y);


