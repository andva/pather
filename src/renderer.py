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

    def update(self, _map, drawClusters):
        self.screen.fill(WHITE)
        self.drawBoard(_map, drawClusters)
        if drawClusters:
            drawGrid(_map)
        pygame.display.update()

    def drawBoard(self, _map):
        widthPerTile = self.SCREEN_WIDTH / _map.width;
        heightPerTile = self.SCREEN_HEIGHT / _map.height;
    # Loop trough all and draw board
        for i in range(0, _map.width):
            for j in range(0, _map.height):
                if _map[[i,j]] == FLOOR:
                    c = BLUE  
                elif _map[[i,j]] == PATH:
                    c = RED;
                else: 
                    c = GREEN;
                p = [i * widthPerTile, j * heightPerTile, 
                     (i+1)*widthPerTile,	(j+1)*heightPerTile];
                pygame.draw.rect(self.screen, c, p, 0)


    def drawGrid(self, map):
        widthPerCluster = self.SCREEN_WIDTH / _map.clusters;
        heightPerCluster = self.SCREEN_HEIGHT / _map.clusters;
        for i in range(0, _map.clusters):
            for j in range(0, _map.clusters):
                p = [i * widthPerCluster, j * heightPerCluster,
                     (i+1) * widthPerCluster, (j+1)*heightPerCluster];
                pygame.draw.rect(self.screen, BLACK, p, 4);

    def drawGraph(self, map):
        return