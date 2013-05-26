# Implementation of near-optimal hierarchical pathfinding

import os, sys
import pygame
from pygame.locals import *

from map import *

W = 24;
H = 24;
SCREEN_WIDTH = 512;
SCREEN_HEIGHT = 512;
NUM_CLUSTERS_PER_DIM = 3;

drawClusters = True;

# Some colors
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]

def drawBoard(_map, screen):
	widthPerTile = SCREEN_WIDTH / _map.width;
	heightPerTile = SCREEN_HEIGHT / _map.height;
	# Loop trough all and draw board
	for i in range(0, _map.width):
		for j in range(0, _map.height):
			if _map[[i,j]] == FLOOR or _map[[i,j]] == PATH:
				c = blue  
			else: 
				c = green;
			p = [i * widthPerTile, j * heightPerTile, 
				(i+1)*widthPerTile,	(j+1)*heightPerTile];
			pygame.draw.rect(screen, c, p, 0);
	if drawClusters:
		widthPerCluster = SCREEN_WIDTH / NUM_CLUSTERS_PER_DIM;
		heightPerCluster = SCREEN_HEIGHT / NUM_CLUSTERS_PER_DIM;
		for i in range(0, NUM_CLUSTERS_PER_DIM):
			for j in range(0, NUM_CLUSTERS_PER_DIM):
				p = [i * widthPerCluster, j * heightPerCluster,
					(i+1) * widthPerCluster, (j+1)*heightPerCluster];
				pygame.draw.rect(screen, black, p, 4);

def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM);
    _map.createEnt();
    pygame.init();
    screen = pygame.display.set_mode((512, 512));
    done = False;
    clock = pygame.time.Clock()
    
    while done == False:
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			done = True;
    	screen.fill(white);
    	###################
    	drawBoard(_map,screen);
    	###################
    	pygame.display.update()
    	# 
    	clock.tick(30)
    return

if __name__ == "__main__":
    main()
