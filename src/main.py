# Implementation of near-optimal hierarchical pathfinding
# import os, sys
usePygame = True;
if usePygame:
    from renderer import Renderer
    from inputhandler import InputHandler
from map import *

W = 40
H = 40
SCREEN_WIDTH = 512;
SCREEN_HEIGHT = 512;
NUM_CLUSTERS_PER_DIM = 5;


drawClusters = True;

def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM);

    # print _map;
    # print _map.graph;
    if (usePygame):
        _inputHandler = InputHandler();
        _renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT);
    done = False;

    while done == False:
    	
    	###################
        if (usePygame):
            done = _renderer.handleEvents()

            _renderer.update(_map, drawClusters)
        else:
            done = True;
    return

if __name__ == "__main__":
    main()
