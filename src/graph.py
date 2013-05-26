class Position:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]";
    def __add__(p1, p2):
        return Position(p1.x + p2.x, p1.y + p2.y);
    def __getitem__(self):
        return [x, y];
    def __len__(self):
        return 2;

class Entrance:
    def __init__(self, mapId1, mapId2):
        self.id1 = mapId1;
        self.id2 = mapId2;
        
class Node:
    def __init__(self, x, y, clusterid):
        self.position = Position(x, y);
        self.clusterid = clusterid;

class Edge:
    def __init__(self, i1, i2, cost):
        self.i1 = i1;
        self.i2 = i2;
        self.cost = cost;
    def __getitem__(self, n):
        if n == 0:
            return self.i1;
        if n == 1:
            return self.i2;
        else:
            raise Exception("Invalid index!");
    def __str__(self):
        return "[" + self.i1 + "," + self.i2 + "]";

class Graph:
    def __init__(self):
        self.nodes = [];
        self.edges = [];

    def addNode(self, position):
        self.nodes.append(position);

    def addEdge(self, node1, node2, cost):
        self.edges.append(Edge(node1, node2, cost));

    def clearGraph(self):
        self.nodes = [];
        del self.edges[:];
