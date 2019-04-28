import curses

class PathFinder:
	def __init__(self, parent):
		self.parent = parent

	def construct_path(self, current_node, start_node):
		new_path = []
		while (current_node != start_node):
			new_path.append(current_node)
			current_node = current_node.parent
		return new_path[::-1]

	def find_path(self, start_node, end_node):
		''' Uses the A* path finding algorithm to find a path, assuming the parent has:
		distance(), return_neighbours()'''
		
		closed_set = []
		open_set = [start_node]
		start_node.hcost = self.parent.distance(start_node, end_node)

		while (len(open_set) != 0):
			current_node = min(open_set, key = lambda x: x.fcost)

			if (current_node == end_node):
				return self.construct_path(end_node, start_node)

			open_set.remove(current_node)
			closed_set.append(current_node)

			for neighbour in self.parent.return_neighbours(current_node):
				if (neighbour in closed_set or not neighbour.walkable):
					continue

				tentative_gcost = current_node.gcost + self.parent.distance(current_node, neighbour)

				if neighbour not in open_set:
					open_set.append(neighbour)
				elif tentative_gcost >= neighbour.gcost:
					continue

				neighbour.parent = current_node
				neighbour.gcost = tentative_gcost
				neighbour.hcost = self.parent.distance(neighbour, end_node)

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
		
class Grid:
	def __init__(self, width, height):
		self.grid = []
		self.width = width
		self.height = height
		self.path_start = None
		self.path_end = None
		self.path = []
		self.path_finder = PathFinder(self)
		for y in range(height):
			self.grid.append([])
			for x in range(width):
				self.grid[y].append(Node(x, y, True))
		
	def draw(self, stdout):
		stdout.addstr(0, 0, "+{}+\n".format('-' *(self.width*2-1)))
		for y in range(self.height):
			stdout.addstr("|")
			for x in range(self.width):
				node = self.grid[y][x]
				char = ' '; colour = 0
				if (node == self.path_start or node == self.path_end):
					char = 'x'; colour = 3
				elif (node in self.path):
					char = ' '; colour = 2
				elif (not node.walkable):
					char = '#'; colour = 1
				stdout.addch(char, curses.color_pair(colour))
				stdout.addch('|')
			stdout.addch('\n') 
		stdout.addstr("+{}+\n".format('-' *(self.width*2-1)))	

	def return_neighbours(self, node):
		neighbours = []
		for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
			nx = node.x + offset[0]
			ny = node.y + offset[1]
			if (nx < 0 or nx >= self.width or ny < 0 or ny >= self.height):
				continue
			neighbours.append(self.grid[ny][nx])
		return neighbours

	def distance(self, node1, node2):
		dif_x = abs(node1.x - node2.x)
		dif_y = abs(node1.y - node2.y)
		return dif_x + dif_y

	def find_path(self):
		new_path = self.path_finder.find_path(self.path_start, self.path_end)	
		if (new_path == None):
			return False
		self.path = new_path
		return True

w = int(input("Grid width : "))
h = int(input("Grid height: "))
g = Grid(w, h)

def display_warning(text, stdout):
	stdout.move(g.height + 2, 0)
	stdout.addstr(text, curses.color_pair(1))
	
def main(stdout):
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
	
	x = 1
	y = 1

	while True:
		x = min(max(x, 1), g.width * 2 - 1)
		y = min(max(y, 1), g.height)

		g.draw(stdout)
		stdout.move(y, x)

		c = stdout.getch()	# Also refreshes console

		stdout.move(g.height + 2, 0)
		stdout.clrtoeol() # Get rid of messages

		if (c == ord('q')):  break 
		elif (c == ord('w')): y -= 1
		elif (c == ord('s')): y += 1
		elif (c == ord('a')): x -= 2
		elif (c == ord('d')): x += 2
		elif (c == ord('z') or c == ord('x')): 
			g_y = y - 1; g_x = (x - 1) // 2
			node = g.grid[g_y][g_x]

			if (node.walkable):
				g.path = []
				if (c == ord('z')):
					g.path_start = node
				elif (c == ord('x')):
					g.path_end = node

		elif (c == ord('c')):
			for nlist in g.grid:
				for node in nlist:
					node.walkable = True
			g.path_start = None
			g.path_end = None
			g.path = []

		elif (c == ord('\n')):
			g_y = y - 1; g_x = (x - 1) // 2
			node = g.grid[g_y][g_x]
			g.path = []
			new_state = not node.walkable
			node.walkable = new_state

			if (node == g.path_start):
				g.path_start = None
			elif (node == g.path_end):
				g.path_end = None

		elif (c == ord('f')):
			if ((g.path_start == None or g.path_end == None)):
				display_warning("Missing start or end node!", stdout)
			else:
				result = g.find_path()
				if (not result): display_warning("No path found", stdout)
				

curses.wrapper(main)