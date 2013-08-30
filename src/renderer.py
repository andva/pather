import pygame
from pygame.locals import *
from globalconsts import *
from map import *

# Some colors


class Renderer:
    def __init__(self, width, height):
        pygame.init();
        self.screen = pygame.display.set_mode((width, height));
        self.clock = pygame.time.Clock();
        self.SCREEN_WIDTH = width;
        self.SCREEN_HEIGHT = height;

    def handleEvents(self):
        for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			return True;
        return False;

    def update(self, board, drawClusters):
        self.screen.fill(WHITE)
        self.drawBoard(board)
        if drawClusters:
            self.drawGrid(board)
        self.drawGraph(board)
        pygame.display.update()

    def drawBoard(self, board):
        widthPerTile = self.tileWidth(board)
        heightPerTile = self.tileHeight(board)
    # Loop trough all and draw board
        for i in range(0, board.width):
            for j in range(0, board.height):
                if board[[i,j]] == FLOOR:
                    c = BLUE  
                elif board[[i,j]] == PATH:
                    c = RED;
                else: 
                    c = GREEN;
                p = [i * widthPerTile, j * heightPerTile, 
                     (i+1)*widthPerTile,	(j+1)*heightPerTile];
                pygame.draw.rect(self.screen, c, p, 0)


    def drawGrid(self, board):
        widthPerCluster = float(self.SCREEN_WIDTH) / float(board.clusters)
        heightPerCluster = float(self.SCREEN_HEIGHT) / float(board.clusters)
        for i in range(0, board.clusters):
            for j in range(0, board.clusters):
                p = [i * widthPerCluster, j * heightPerCluster,
                     (i+1) * widthPerCluster, (j+1)*heightPerCluster];
                pygame.draw.rect(self.screen, BLACK, p, 4);

    def drawGraph(self, board):

        for edge in board.graph.edges:
            p = [[],[]]
            for i in range(0, 2):
                p[i] = self.calculateCenterOfNode(board, edge[i].position)
                    
            pygame.draw.aaline(self.screen, BLACK, p[0], p[1])
        return

    def tileWidth(self, board):
        return float(self.SCREEN_WIDTH) / float(board.width)

    def tileHeight(self, board):
        return float(self.SCREEN_HEIGHT) / float(board.height)

    # Position is position of corner of tile in board coordinates
    def calculateCenterOfNode(self, board, position):
        widthPerTile = self.tileWidth(board)
        heightPerTile = self.tileHeight(board)

        return ([widthPerTile * position.x + float(widthPerTile) / 2.0, 
                heightPerTile * position.y + float(heightPerTile) / 2.0])