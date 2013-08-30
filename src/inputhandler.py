import pygame
from pygame.locals import *
from graph import Position
LEFT_MOUSE_BUTTON = 0
RIGHT_MOUSE_BUTTON = 2

class InputHandler:
	def __init__(self, screenWidth, screenHeight, boardWidth, boardHeight):
		self.isDown = [False] * 500
		self.mouseIsDown = [False] * 3
		self.shiftMouseDown = [False] * 3
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.boardWidth = boardWidth
		self.boardHeight = boardHeight

	def getMousePressed(self, key, shift = False):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		keys = pygame.mouse.get_pressed()

		if shift:
			extra = pygame.key.get_mods() & KMOD_SHIFT
			b = self.fixKeys(keys, key, self.shiftMouseDown, extra)

		else:
			extra = not (pygame.key.get_mods() & KMOD_SHIFT)
			b = self.fixKeys(keys, key, self.shiftMouseDown, extra)
		
		return b

	def getMousePressedWithShift(self, key):
		if key > 2:
			raise Exception("getPressed key not in allowed range!")
		keys = pygame.mouse.get_pressed()
		extraCheck = pygame.key.get_mods() & KMOD_SHIFT
		b = self.fixKeys(keys, key, self.shiftMouseDown, extraCheck)
		return b

	def getKeyPressed(self, key):
		keys = pygame.key.get_pressed()		
		return self.fixKeys(keys, key, self.isDown)

	def getMousePosition(self, board):
		plist = pygame.mouse.get_pos();
		return self.convertScreenToBoard(Position(plist[0], plist[1]), board)

	def fixKeys(self, keys, key, array, extraCheck = True):
		down = keys[key]
		r = not down and array[key] and extraCheck
		if extraCheck:
			array[key] = down
		return r

	def convertScreenToBoard(self, position, board):
		tileWidth = float(self.screenWidth) / float(board.width)
		tileHeight = float(self.screenHeight) / float(board.height)
		boardPos = Position(int(position.x / tileWidth), int(position.y / tileHeight))
		return boardPos