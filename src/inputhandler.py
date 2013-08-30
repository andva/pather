import pygame
from pygame.locals import *

LEFT_MOUSE_BUTTON = 0
RIGHT_MOUSE_BUTTON = 2

class InputHandler:
	def __init__(self):
		self.isDown = [False] * 500
		pass

	def getMousePressed(self, key):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		return pygame.mouse.get_pressed()[key] and not (pygame.key.get_mods() & KMOD_SHIFT)

	def getMousePressedWithShift(self, key):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		return pygame.mouse.get_pressed()[key] and (pygame.key.get_mods() & KMOD_SHIFT)

	def getKeyPressed(self, key):
		keys = pygame.key.get_pressed()
		down = keys[key]
		r = (not down and self.isDown[key])
		self.isDown[key] = down
		return r
