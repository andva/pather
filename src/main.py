# Implementation of near-optimal hierarchical pathfinding
# import os, sys
usePygame = True;
if usePygame:
    from renderer import Renderer
    from inputhandler import *
from map import *
from player import *
W = 30
H = 30
SCREEN_WIDTH = 512;
SCREEN_HEIGHT = 512;
NUM_CLUSTERS_PER_DIM = 5;

def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM);

    drawClusters = False;
    drawGraph = False;

    if (usePygame):
        _inputHandler = InputHandler();
        _renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT);
    done = False;

    while done == False:
    	
    	###################
        if (usePygame):
            done = _renderer.handleEvents()
            if _inputHandler.getKeyPressed(K_c):
                drawClusters = not drawClusters
            if _inputHandler.getKeyPressed(K_g):
                drawGraph = not drawGraph

            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON):
                print("Left mouse")
            _renderer.update(_map, drawClusters, drawGraph)
        else:
            done = True;
    return

if __name__ == "__main__":
    main()
