class game:
	def __init__(self, gameID, password):
		self.gameID = gameID
		self.password = password
		self.gameState = 0
		self.users = []
		self.maxUsers = 4
		self.turn = 0

		print("Created Game with ID:",self.gameID, "and password:", self.password)

	def __str__(self):
		return "gameID: {0}, players:{1}".format(str(self.gameID), str(self.users))

	def __repr__(self):
		return str(self)