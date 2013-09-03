class Player:
    def __init__(self, position, currentCluster, goal = None, path = None, name = None):
        self.position = position
        self.currentCluster = currentCluster
        self.goal = goal
        self.name = name
        self.path = path

    def __str__(self):
        return "Player " + str(self.name) + " [" + str(self.position) + ", " + str(self.goal) + "]"

    def updatePosition(self, position):
        self.position = position

    def updateGoal(self, goal):
        self.goal = goal

    def walk(self):
        if self.position is not self.goal:
            self.position = self.path.popNextPosition()
