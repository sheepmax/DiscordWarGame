import pygame
from units import Unit
from battlefields import Battlefield
import interface
import threading
from glob import glob
import json

TILE_SIZE = 45

pygame.display.init()

running = True

screen = pygame.display.set_mode((1, 1))
previous_drawn = None
WIN_WIDTH = 0
WIN_HEIGHT = 0

textures = {}

def load_textures ():
	''' Loads texture data for battlefield drawing '''
	for texture_file in glob("Tiles\\[0-9]*.png"):
		split_path = texture_file.split('_')
		texture_number = int(split_path[0][6:])
		mode = split_path[1]
		texture = pygame.image.load(texture_file)
		if (mode == 't'): converted = texture.convert_alpha()
		else: converted = texture.convert() 
		textures[texture_number] = [converted, texture.get_height() - 45] # Surface, offset from base height

def load_unit_data ():
	''' Loads unit data into Unit class'''
	for unit_file_path in glob("Units\\*.json"):
		with open(unit_file_path, "r") as unit_file:
			name = unit_file_path[6:-5]
			Unit.unit_types[name] = json.load(unit_file)
			icon = pygame.image.load("Units\\{}".format(Unit.unit_types[name]["icon"]))
			Unit.unit_types[name]["icon"] = icon.convert_alpha()

def draw_battlefield (battlefield):
	global screen, previous_drawn, WIN_WIDTH, WIN_HEIGHT
	if (previous_drawn != battlefield.ID):
		WIN_WIDTH = battlefield.width * (TILE_SIZE + 1) + 1
		WIN_HEIGHT = battlefield.height * (TILE_SIZE + 1) + 1
		screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		previous_drawn = battlefield.ID

	screen.fill((255, 255, 255))
	for x in range(battlefield.width + 1):
		pygame.draw.line(screen, (0, 0, 0), (0, x * (TILE_SIZE + 1)), (WIN_WIDTH, x * (TILE_SIZE + 1)))

	for y in range(battlefield.height + 1):
		pygame.draw.line(screen, (0, 0, 0), (y * (TILE_SIZE + 1), 0), (y * (TILE_SIZE + 1), WIN_HEIGHT))

	for x in range(battlefield.width):
		for y in range(battlefield.height):
			background_tile_num = battlefield.background_tiles[y][x]
			blit_coordinates = [x * (TILE_SIZE + 1) + 1, y * (TILE_SIZE + 1) + 1]
			# 0 = no tile
			if (background_tile_num):
				screen.blit(textures[background_tile_num - 1][0], blit_coordinates)
			base_tile_num = battlefield.base_map[y][x]
			base_tile_data = textures[base_tile_num]
			if (base_tile_data[1] != 0): blit_coordinates[1] -= base_tile_data[1]
			screen.blit(base_tile_data[0], blit_coordinates)


	for unit_key in battlefield.units:
		unit = battlefield.units[unit_key]
		icon = Unit.unit_types[unit.name]["icon"]
		screen.blit(icon, (unit.position[0] * (TILE_SIZE + 1) + 1, unit.position[1] * (TILE_SIZE + 1) + 1))

load_textures()
load_unit_data()

battlefields_available = [Battlefield("mock_battlefield.json"), Battlefield("mock_battlefield.json"),
						  Battlefield("mock_battlefield.json"), Battlefield("mock_battlefield.json")]  

current_battlefield = battlefields_available[0]

interface_thread = threading.Thread(target = interface.get_input)
interface_thread.daemon = True
interface_thread.start()

while running:

	draw_battlefield(current_battlefield)
	pygame.display.update()

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			pygame.quit()
			running = False