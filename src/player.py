class Player:
	def __init__(self, position, goal = None, name = None):
		self.position = position
		self.goal = goal
		self.name = name

	def __str__(self):
		return "Player " + str(self.name) + " [" + str(self.position) + ", " + str(self.goal) + "]"

	def updatePosition(self, position):
		self.position = position

	def updateGoal(self, goal):
		self.goal = goal
