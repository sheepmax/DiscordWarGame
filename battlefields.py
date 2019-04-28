from utils import *
import time

class Battlefield:
	num_fields = 0

	def __init__(self, config):
		load_class(self, config)
		self.ID = Battlefield.num_fields
		Battlefield.num_fields += 1

	def co_to_key(self, coordinates):
		return (coordinates[1] * self.width + coordinates[0])

	def save_path(self):
		localtime = "{}_{}_{}_{}_{}".format(time.strftime("%d"), time.strftime("%m"),
											time.strftime("%Y"), time.strftime("%H"), time.strftime("%M"))
		name = self.name.replace(' ', '_')
		file_path = "save_{}_{}.txt".format(name, localtime)
		return file_path

	def add_unit (self, unit):
		self.units[self.co_to_key(unit.position)] = unit

	def is_unit (self, position):
		return (self.co_to_key(position) in self.units)

	def return_unit(self, position):
		if (not self.is_unit(position)): return None
		return self.units[self.co_to_key(position)]

	def in_bounds(self, position):
		return (position[0] >= 0 and position[0] < self.width and
				position[1] >= 0 and position[1] < self.height)

	def move_unit (self, initial, final):
		init_key = self.co_to_key(initial)
		final_key = self.co_to_key(final)

		self.units[init_key].position[:] = final
		self.units[final_key] = self.units.pop(init_key)



