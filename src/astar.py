class AStar:
	def __init__(self, gameMap):
		self.gameMap = gameMap;

	def findMinimum(self, nodes):
		n = nodes[0];
		for i in range(0, nodes.length()):
			if(nodes[i].cost < n.cost):
				n = nodes[i];
		return n;


	def solveBetweenNodes(self, clusterId, nodeA, goal):
		visitedPositions = [];
		start = Node(nodeA.position, clusterId, 0);
		stack = [start];
		while stack.length() > 0:
			# Find minimum active node
			currentNode = findMinimum(stack);

			


	# Manhattan distance between nodes
	def calculateHeuristic(self, node, goal):
		x = node.position.x - goal.position.x;
		y = node.position.y - goal.position.y;

		return abs(x) + abs(y);


