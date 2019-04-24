import utils
import time


class Battlefield:
	num_fields = 0
	def __init__(self, config):
		utils.load_class(self, config)
		self.ID = Battlefield.num_fields
		Battlefield.num_fields += 1

	def save_path(self):
		localtime = "{}_{}_{}_{}_{}".format(time.strftime("%d"), time.strftime("%m"),
											time.strftime("%Y"), time.strftime("%H"), time.strftime("%M"))
		name = self.name.replace(' ', '_')
		file_path = "save_{}_{}.txt".format(name, localtime)
		return file_path

	def add_unit (self, unit):
		key = unit.position[1] * self.width + unit.position[0]
		self.units[key] = (unit)

	def move_unit (self, initial, final):
		init_key = initial[1] * self.width + initial[1]
		final_key = final[1] * self.width + final[1]

		self.units[init_key].position[:] = final
		self.units[final_key] = self.units.pop(init_key)



