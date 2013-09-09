# Implementation of near-optimal hierarchical pathfinder
import os, sys
usePygame = True
if usePygame:
    from renderer import Renderer
    from inputhandler import *
from map import *
from player import *
W = 6
H = 6
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
NUM_CLUSTERS_PER_DIM = 2

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
    running = True # Responsible for deciding if we are updating the position of the players

    while not done:

        ###################
        if usePygame:

            done = _renderer.handleEvents()

            if _inputHandler.getKeyPressed(K_c):
                drawClusters = not drawClusters

            if _inputHandler.getKeyPressed(K_g):
                drawGraph = not drawGraph

            if _inputHandler.getKeyPressed(K_r):
                edgesToRemove = []
                nodesToRemove = []
                for node in _map.graph.nodes:
                    # Cheat to remove all nodes.
                    tester = False
                    for id in node.affectedPlayers:
                        if id == ALL_PLAYERS:
                            tester = True
                    if not tester:
                        for edge in _map.graph.edges:
                            if edge.i1 == node or edge.i2 == node:
                                edgesToRemove.append(edge)
                                nodesToRemove.append(node)
                for edge in edgesToRemove:
                    try:
                        _map.graph.edges.remove(edge)
                    except ValueError:
                        pass
                for node in nodesToRemove:
                    try:
                        _map.graph.nodes.remove(node)
                    except ValueError:
                        pass
                players = []
                activePlayer = -1

            if _inputHandler.getKeyPressed(K_t):
                if activePlayer >= 0:
                    player = players[activePlayer]
                    if player.goal != None:
                        _map.removeInGraph(player, player.goal.position)
                    _map.removeInGraph(player, player.start.position)

                    players.pop(activePlayer)
                    activePlayer = activePlayer - 1

            if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON, True):
                mousePosition = _inputHandler.getMousePosition(_map)

                if (_map.isPositionValid(mousePosition) and
                    _map[mousePosition.x, mousePosition.y] != WALL):

                    cid = _map.convertMapv2ClusterId(mousePosition)
                    playerId = len(players)
                    activePlayer = playerId
                    player = Player(mousePosition, cid, playerId)
                    players.append(player)

                    _map.addAndConnectNodeToGraph(player.start)

                    print("Added player" + str(playerId))
                else:
                    print("Cant add player on " + str(mousePosition) + " " +
                          str(_map.isPositionValid(mousePosition)) + " " + str(_map[mousePosition.x, mousePosition.y] != WALL))

            if activePlayer != -1:
                if _inputHandler.getKeyPressed(K_n):
                    activePlayer = (activePlayer + 1) % len(players)


                if _inputHandler.getMousePressed(LEFT_MOUSE_BUTTON):
                    mousePosition = _inputHandler.getMousePosition(_map)
                    if (_map.isPositionValid(mousePosition) and
                                                       _map[mousePosition.x, mousePosition.y] != WALL):

                        if player.start is not None:
                            _map.removeAllRef(player)
                            cid = _map.convertMapv2ClusterId(mousePosition)
                            players[activePlayer].updateStart(mousePosition, cid)
                            _map.addAndConnectNodeToGraph(players[activePlayer].start)
                            _map.addAndConnectNodeToGraph(players[activePlayer].goal)
                            if player.goal is not None:
                                player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)
                                if player.path is None:
                                    print "ERROR ERROR ERROR"
                                    # _map.addAndConnectNodeToGraph(players[activePlayer].start)
                                    # _map.addAndConnectNodeToGraph(players[activePlayer].goal)
                                    # player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)

                if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON):
                    mousePosition = _inputHandler.getMousePosition(_map)
                    if (_map.isPositionValid(mousePosition) and
                                                       _map[mousePosition.x, mousePosition.y] != WALL):
                        player = players[activePlayer]
                        # Delete old goal
                        _map.removeAllRef(player)

                        # Add new goal
                        cid = _map.convertMapv2ClusterId(mousePosition)
                        player.updateGoal(mousePosition, cid)

                        _map.addAndConnectNodeToGraph(players[activePlayer].goal)
                        _map.addAndConnectNodeToGraph(players[activePlayer].start)

                        player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)
                        # if player.path == None:
                            # _map.addAndConnectNodeToGraph(players[activePlayer].start)
                            # _map.addAndConnectNodeToGraph(players[activePlayer].goal)
                            # player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)

                if _inputHandler.getKeyPressed(K_s):
                    for player in players:
                        player.walk()
            _renderer.update(_map, players, activePlayer, drawClusters, drawGraph)
        else:
            done = True
    return

if __name__ == "__main__":
    main()
