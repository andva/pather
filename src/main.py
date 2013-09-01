# Implementation of near-optimal hierarchical pathfinder
# import os, sys
usePygame = True
if usePygame:
    from renderer import Renderer
    from inputhandler import *
from map import *
from player import *
W = 50
H = 50
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
NUM_CLUSTERS_PER_DIM = 10

def main():
    _map = Map(W, H, NUM_CLUSTERS_PER_DIM)

    drawClusters = False
    drawGraph = False
    players = []
    activePlayer = -1

    if usePygame:
        _inputHandler = InputHandler(SCREEN_WIDTH, SCREEN_HEIGHT, W, H)
        _renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT)

    done = False

    while not done:

        ###################
        if usePygame:
            updatedPlayer = False

            done = _renderer.handleEvents()

            if _inputHandler.getKeyPressed(K_c):
                drawClusters = not drawClusters

            if _inputHandler.getKeyPressed(K_g):
                drawGraph = not drawGraph

            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON):
                mousePosition = _inputHandler.getMousePosition(_map)
                if activePlayer != -1 and (_map.isPositionValid(mousePosition) and
                                                   _map[mousePosition.x, mousePosition.y] != WALL):
                    players[activePlayer].position = mousePosition
                    updatedPlayer = True

            if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON):
                mousePosition = _inputHandler.getMousePosition(_map)
                if activePlayer != -1 and (_map.isPositionValid(mousePosition) and
                                                   _map[mousePosition.x, mousePosition.y] != WALL):
                    players[activePlayer].goal = mousePosition
                    updatedPlayer = True

            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON, True):
                mousePosition = _inputHandler.getMousePosition(_map)
                cid = 0
                if (_map.isPositionValid(mousePosition) and
                    _map[mousePosition.x, mousePosition.y] != WALL):
                    players.append(Player(mousePosition, cid))
                    activePlayer = len(players) - 1
                    print("Added player" + str(activePlayer))
                else:
                    print("Cant add player on " + str(mousePosition) + " " +
                          str(_map.isPositionValid(mousePosition)) + " " + str(_map[mousePosition.x, mousePosition.y] != WALL))
            if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON, True):
                if activePlayer != -1:
                    pass
                print("S right")

            if updatedPlayer:
                pass

            _renderer.update(_map, players, activePlayer, drawClusters, drawGraph)
        else:
            done = True
    return

if __name__ == "__main__":
    main()
