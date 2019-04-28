class Node:
	def __init__(self, x, y, walkable):
		self.x = x
		self.y = y
		self.walkable = walkable
		self.parent = None
		self.gcost = 0
		self.hcost = 0

	@property
	def fcost(self):
		return self.gcost + self.hcost

existing_nodes = []

def get_neighbours(node, battlefield, illegals, u_range, start):
	global existing_nodes
	neighbours = []
	for offset in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
		neighbour_x = node.x + offset[0]
		neighbour_y = node.y + offset[1]

		if (get_distance(node, start) > u_range): continue

		if (not battlefield.in_bounds([neighbour_x, neighbour_y])): continue
		walkable = not (battlefield.base_map[neighbour_y][neighbour_x] in illegals) 

		for node in existing_nodes:
			if (node.x == neighbour_x and node.y == neighbour_y):
				node.walkable = walkable
				neighbours.append(node)
			else:
				new_node = Node(neighbour_x, neighbour_y, walkable)
				neighbours.append(new_node)
				existing_nodes.append(new_node)
	return neighbours            


def find_path(start, finish, u_range, battlefield, illegals):
	global existing_nodes
	start_node = Node(start[0], start[1], True)
	end_node = Node(finish[0], finish[1], True)
	existing_nodes += [start_node, end_node]
	openset = []
	closedset = []
	openset.append(start_node)

	while (len(openset) > 0):
		current_node = openset[0]
		for node in openset:
			if (node.fcost < current_node.fcost or
			   (node.fcost == current_node.fcost and node.hcost < current_node.hcost)):
				current_node = node 

		openset.remove(current_node)
		closedset.append(current_node)

		if (current_node == end_node): 
			return retrace_path(start_node, end_node)

		for neighbour in get_neighbours(current_node, battlefield, illegals, u_range, start_node):
			if (not neighbour.walkable or neighbour in closedset): 
				continue
			new_movement_cost_to_neighbour = current_node.gcost + get_distance(current_node, neighbour)

			if (new_movement_cost_to_neighbour < neighbour.gcost or neighbour not in openset):
				neighbour.gcost = new_movement_cost_to_neighbour
				neighbour.hcost = get_distance(neighbour, end_node)
				neighbour.parent = current_node

				if (neighbour not in openset):
					openset.append(neighbour)


def retrace_path (start_node, end_node):
	path = []
	current_node = end_node

	while (current_node != start_node):
		path.append(current_node)
		current_node = current_node.parent

	return path


def path_is_valid(start, finish, u_range, battlefield, illegals):
	pass

def get_distance (node1, node2):
	relative_x = abs(node1.x - node2.x)
	relative_y = abs(node1.y - node2.y)
	return relative_x + relative_y

