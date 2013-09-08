# Implementation of near-optimal hierarchical pathfinder
# import os, sys
usePygame = True
if usePygame:
    from renderer import Renderer
    from inputhandler import *
from map import *
from player import *
W = 24
H = 24
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
NUM_CLUSTERS_PER_DIM = 4

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
                            for node in _map.graph.nodes:
                                if node.position == player.start.position:
                                    t1 = False
                                    t2 = False
                                    for id in node.affectedPlayers:
                                        if id == player.id:
                                            # This should be removed
                                            t2 = True
                                        else:
                                            t = True
                                    if t1 and not t2:
                                        node.affectedPlayers.remove(player.id)
                                    elif not t1 and t2:
                                        # Remove all edges with node
                                        edgesToRemove = []
                                        for edge in _map.graph.edges:
                                            if edge.i1 == node or edge.i2 == node:
                                                edgesToRemove.append(edge)
                                        for edge in edgesToRemove:
                                            _map.graph.edges.remove(edge)
                                        _map.graph.nodes.remove(node)

                        cid = _map.convertMapv2ClusterId(mousePosition)
                        players[activePlayer].updateStart(mousePosition, cid)
                        _map.addAndConnectNodeToGraph(players[activePlayer].start)
                        if player.goal is not None:
                            player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)

                if _inputHandler.getMousePressed(RIGHT_MOUSE_BUTTON):
                    mousePosition = _inputHandler.getMousePosition(_map)
                    if (_map.isPositionValid(mousePosition) and
                                                       _map[mousePosition.x, mousePosition.y] != WALL):
                        player = players[activePlayer]
                        # Delete old goal
                        if player.goal is not None:
                            for node in _map.graph.nodes:
                                if node.position == player.goal.position:
                                    t1 = False
                                    t2 = False
                                    for id in node.affectedPlayers:
                                        if id == player.id:
                                            t2 = True
                                        else:
                                            t1 = True
                                    if t1 and t2:
                                        node.affectedPlayers.remove(player.id)
                                    elif not t1 and t2:
                                        # Remove all edges with node
                                        edgesToRemove = []
                                        for edge in _map.graph.edges:
                                            if edge.i1 == node or edge.i2 == node:
                                                edgesToRemove.append(edge)
                                        for edge in edgesToRemove:
                                            _map.graph.edges.remove(edge)
                                        _map.graph.nodes.remove(node)

                        # Add new goal
                        cid = _map.convertMapv2ClusterId(mousePosition)
                        player.updateGoal(mousePosition, cid)
                        _map.addAndConnectNodeToGraph(players[activePlayer].goal)
                        player.path = _map.calculatePathInGraph(player.start, player.goal, player.id)
                for player in players:
                    # player.walk()
                    pass
            _renderer.update(_map, players, activePlayer, drawClusters, drawGraph)
        else:
            done = True
    return

if __name__ == "__main__":
    main()
