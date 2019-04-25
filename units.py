import json

class Unit:
	unit_types = {}
	def __init__(self, name, position, owner):
		self.name = name     # Data can be retrieved through this
		self.owner = owner
		self.position = position
		self.health = Unit.unit_types[name]["health"]

	def save (self):
		file_path = "{}_{}_{}_{}".format(self.name, self.owner, self.position[0], self.position[1])
		return file_path
