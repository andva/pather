# Implementation of near-optimal hierarchical pathfinding
# import os, sys
usePygame = True;
if usePygame:
    from renderer import Renderer
    from inputhandler import *
from map import *
from player import *
W = 50
H = 50
SCREEN_WIDTH = 512;
SCREEN_HEIGHT = 512;
NUM_CLUSTERS_PER_DIM = 10;

def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM);

    drawClusters = False
    drawGraph = False
    players = []
    activePlayer = -1
    
    if (usePygame):
        _inputHandler = InputHandler()
        _renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT, _map.width)
    
    done = False

    while done == False:
    	
    	###################
        if (usePygame):
            updatedPlayer = False

            done = _renderer.handleEvents()
            
            if _inputHandler.getKeyPressed(K_c):
                drawClusters = not drawClusters
            
            if _inputHandler.getKeyPressed(K_g):
                drawGraph = not drawGraph

            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON):
                if activePlayer != -1:
                    players[activePlayer].position = _inputHandler.getMousePosition()
                    updatedPlayer = True
                print("Left mouse")
            
            if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON):
                print("Right mouse")
            
            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON, True):
                mousePosition = _inputHandler.getMousePosition()
                cid = 0
                players.append(Player(mousePosition, cid))
                activePlayer = len(players) - 1
                print("Added player" + str(activePlayer))
            
            if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON, True):
                if activePlayer != -1:
                    pass
                print("S right")
            
            _renderer.update(_map, players, activePlayer, drawClusters, drawGraph)
        else:
            done = True;
    return

if __name__ == "__main__":
    main()
