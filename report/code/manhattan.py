def calculateManhattanDistance(self, node, goal):
    goalToNode = nodePos - goal
    return abs(goalToNode.x) + abs(goalToNode.y)
