from pygame import event, USEREVENT

command_data = {"move": [0, ["cinitial", "cfinal"]], "add_unit": [1, ["sunit_name", "cposition"]],
				"info": [2, ["cposition", "sinfo_type"]]}
coordinate_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']

def parse_coordinates(co_string):
	coordinate = [0, 0]
	if (len(co_string) < 2 or len(co_string) > 3): return None
	try:
		if (co_string[0] in coordinate_alphabet): 
			coordinate[0] = coordinate_alphabet.index(co_string[0])
			coordinate[1] = int(co_string[1:]) - 1
		else:
			coordinate[0] = coordinate_alphabet.index(co_string[-1])
			coordinate[1] = int(co_string[0:-1]) - 1
	except: return None
	return coordinate

def parse_input(command):
	command = command.split()
	if (len(command) == 0 or command[0] not in command_data): return None

	type_offset = command_data[command[0]][0]
	event_type = USEREVENT + type_offset
	event_attributes = {}

	parameter_templates = command_data[command[0]][1]
	for index in range(len(parameter_templates)):
		parameter_type = parameter_templates[index][0]
		parameter_name = parameter_templates[index][1:]
		parameter = command[index + 1]

		if (parameter_type == 'c'): 
			parsed_coordinates = parse_coordinates(parameter)
			if (parsed_coordinates == None): return None
			event_attributes[parameter_name] = parsed_coordinates

		elif (parameter_type == 's'):
			event_attributes[parameter_name] = parameter
	return event_type, event_attributes



def get_input():
	while True:
		command = input("--> ")

		result = parse_input(command[1:])
		if (result == None): 
			print("Invalid command")
			continue
		to_post = event.Event(result[0], result[1])
		print(to_post)
		event.post(to_post)


