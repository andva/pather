# Implementation of near-optimal hierarchical pathfinding


# import os, sys

from map import *

W = 30;
H = 30;
SCREEN_WIDTH = 512;
SCREEN_HEIGHT = 512;
NUM_CLUSTERS_PER_DIM = 3;

usePygame = False;
drawClusters = True;

# Some colors
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]



def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM);
    _map.createEnt();

    # print _map;
    print _map.graph;
    if (usePygame):
        _renderer = Renderer();
    done = False;
    while done == False:
    	
    	###################
        if (usePygame):
            done = _renderer.handleEvents();
            _renderer.update(_map);
        else:
            done = True;
    return

if __name__ == "__main__":
    main()
