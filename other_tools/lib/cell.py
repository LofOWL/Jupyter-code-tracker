

class Cell:
	
	def __init__(self):
		self.type = None
		self.index = None
		self.lines = None
	
	def __str__(self):
		return f'{self.type} {self.index} {self.lines}'


if __name__ == "__main__":
	print("cell")
