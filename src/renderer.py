import pygame

from globalconsts import *
from pygame.gfxdraw import aacircle


class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.CIRCLE_SIZE = int(10 / 3.0)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def update(self, board, players, activePlayer, drawClusters, drawGraph):
        self.screen.fill(WHITE)
        self.drawBoard(board)
        self.drawPlayers(board, players, activePlayer)
        if drawClusters:
            self.drawGrid(board)
        if drawGraph:
            self.drawGraph(board)

        pygame.display.update()

    def drawBoard(self, board):
        widthPerTile = self.tileWidth(board)
        heightPerTile = self.tileHeight(board)
        # Loop trough all and draw board
        for i in range(0, board.width):
            for j in range(0, board.height):
                if board[[i, j]] == FLOOR or board[[i, j]] == PATH:
                    c = FLOOR_COLOR
                else:
                    c = WALL_COLOR
                p = [i * widthPerTile, j * heightPerTile,
                     (i + 1) * widthPerTile, (j + 1) * heightPerTile]
                pygame.draw.rect(self.screen, c, p, 0)

    def drawGrid(self, board):
        widthPerCluster = float(self.SCREEN_WIDTH) / float(board.clusters)
        heightPerCluster = float(self.SCREEN_HEIGHT) / float(board.clusters)
        for i in range(0, board.clusters):
            for j in range(0, board.clusters):
                p = [i * widthPerCluster, j * heightPerCluster,
                     (i + 1) * widthPerCluster, (j + 1) * heightPerCluster]
                pygame.draw.rect(self.screen, CLUSTER_EDGE_COLOR, p, 4)

    def drawGraph(self, board):
        for edge in board.graph.edges:
            p = [[], []]
            for i in range(0, 2):
                p[i] = self.calculateCenterOfNode(board, edge[i].position)

            pygame.draw.aaline(self.screen, GRAPH_EDGE_COLOR, p[0], p[1])

        for node in board.graph.nodes:
            p = self.calculateCenterOfNode(board, node.position)
            c = NODE_COLOR
            for pId in node.affectedPlayers:
                if pId is not ALL_PLAYERS:
                    c = ACTIVE_NODES
            pygame.gfxdraw.aacircle(self.screen,
                                    int(p[0]),
                                    int(p[1]),
                                    self.CIRCLE_SIZE, c)
        return

    def drawPlayers(self, board, players, activePlayer):
        for i, player in enumerate(players):
            # Draw player path

            pos = self.calculateCenterOfNode(board, player.position)
            if i == activePlayer:
                c2 = OLIVE
                color = ACTIVE_PLAYER_COLOR
            else:
                c2 = LIGHT_PINK
                color = PLAYER_COLOR
            if player.path != None:
                if player.path.array != None:
                    for nodePos in player.path.array:
                        position = self.calculateCenterOfNode(board, nodePos)
                        pygame.gfxdraw.filled_circle(self.screen, int(position[0]), int(position[1]),
                                                     int(self.CIRCLE_SIZE / 2.0), c2)
            pygame.gfxdraw.aacircle(self.screen, int(pos[0]), int(pos[1]),
                                    self.CIRCLE_SIZE, color)

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