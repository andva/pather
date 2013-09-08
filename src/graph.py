class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"
    def __add__(self, p2):
        return Position(self.x + p2.x, self.y + p2.y)
    def __getitem__(self):
        return [self.x, self.y]
    def __len__(self):
        return 2
    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

class Entrance:
    def __init__(self, mapId1, mapId2):
        self.id1 = mapId1
        self.id2 = mapId2
        
class Node:

    def __init__(self, position, clusterId, affectedPlayers, cost = None, length = None, parentId = None):
        assert isinstance(position, (Position, None))
        self.position = position

        assert isinstance(clusterId, (int, long, None))
        self.clusterId = clusterId

        self.affectedPlayers = affectedPlayers

        if cost is not None:
            assert isinstance(cost, (int, long))
        self.cost = cost

        if length is not None:
            assert isinstance(length, (int, long, None))
        self.length = length

        if parentId is not None:
            assert isinstance(parentId, (int, long, None))
        self.parentId = parentId

    def __str__(self):
        v = "N:" + str(self.clusterId) + " " + str(self.position)
        if self.cost is not None:
            v += " " + self.cost
            v += " " + self.length
        return v

class Edge:
    def __init__(self, i1, i2, cost):
        self.i1 = i1 # Node 1
        self.i2 = i2 # Node 2
        self.cost = cost # Cost for traveling between nodes

    def __eq__(self, edge):

        if ((edge.i1 == self.i1 and edge.i2 == self.i2) or
           (edge.i2 == self.i1 and edge.i1 == self.i2)) :
            return True
        return False

    def __getitem__(self, n):
        if n == 0:
            return self.i1
        if n == 1:
            return self.i2
        else:
            raise Exception("Invalid index!")
    def __str__(self):
        return "[" + str(self.i1) + ", " + str(self.i2) + "]"

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def __str__(self):
        nv = ""
        nv += self.nodesAsString()
        nv += self.edgesAsString()
        return nv

    def nodesAsString(self):
        nv = ""
        for n in self.nodes:
            nv += str(n) + "\n"
        return nv

    def edgesAsString(self):
        res = ""
        for e in self.edges:
            res += str(e) + "\n"
        return res

    def addNode(self, node):
        # Only add if node does not already exists
        for n in self.nodes:
            if n.position == node.position:
                return False
        self.nodes.append(node)
        return True

    def addEdge(self, node1, node2, cost):
        for e in self.edges:
            if Edge(node1, node2, cost) == e:
                return
        self.edges.append(Edge(node1, node2, cost))

    def clearGraph(self):
        self.nodes = []
        del self.edges[:]

    def getNodesInCluster(self, clusterId):
        clusterNodes = []
        for node in self.nodes:
            if node.clusterId == clusterId:
                clusterNodes.append(node)
        return clusterNodes
