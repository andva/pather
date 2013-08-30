import pygame
from pygame.locals import *

LEFT_MOUSE_BUTTON = 0
RIGHT_MOUSE_BUTTON = 2

class InputHandler:
	def __init__(self):
		pass

	def getPressed(self, key):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		return pygame.mouse.get_pressed()[key] and not (pygame.key.get_mods() & KMOD_SHIFT)

	def getPressedWithShift(self, key):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		return pygame.mouse.get_pressed()[key] and (pygame.key.get_mods() & KMOD_SHIFT)

