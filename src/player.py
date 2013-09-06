from graph import Node

class Player:
    def __init__(self, position, currentCluster, playerId, goal = None, goalClusterId = None, path = None, name = None):
        self.position = position
        self.id = playerId
        self.currentCluster = currentCluster
        self.name = name
        self.path = path

        if goal is not None and goalClusterId is not None:
            self.goal = self.updateGoal(goal, goalClusterId)
        else:
            self.goal = None
        self.start = self.updateStart()

    def __str__(self):
        return "Player " + str(self.name) + " [" + str(self.position) + ", " + str(self.goal) + "]"

    def updatePosition(self, position):
        self.position = position

    def updateGoal(self, goalPosition, goalClusterId):
        self.goal = Node(goalPosition, goalClusterId, [self.id])
        return self.goal

    def updateStart(self):
        """
        Updates start node for player.
        Requires position, currentCluster and id to be set.

        :return: self.start
        """
        self.start = Node(self.position, self.currentCluster, [self.id])

        return self.start

    def walk(self):
        if self.position is not self.goal:
            self.position = self.path.popNextPosition()
