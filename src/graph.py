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

    # def __init__(self, position, clusterId):
    #     self.position = position
    #     self.clusterId = clusterId

    def __init__(self, position, clusterId, cost = None):
        self.position = position;
        self.clusterId = clusterId;
        self.cost = cost;

    def __str__(self):
        return "N:" + str(self.clusterId) + " " + str(self.position);

class Edge:
    def __init__(self, i1, i2, cost):
        self.i1 = i1;
        self.i2 = i2;
        self.cost = cost;

    def __eq__(self, edge):

        if ((edge.i1 == self.i1 and edge.i2 == self.i2) or
           (edge.i2 == self.i1 and edge.i1 == self.i2)) :
            return True;
        return False;

    def __getitem__(self, n):
        if n == 0:
            return self.i1;
        if n == 1:
            return self.i2;
        else:
            raise Exception("Invalid index!");
    def __str__(self):
        return "[" + str(self.i1) + ", " + str(self.i2) + "]";

class Graph:
    def __init__(self):
        self.nodes = [];
        self.edges = [];

    def __str__(self):
        nv = "";
        nv += self.nodesAsString();
        nv += self.edgesAsString();
        return nv

    def nodesAsString(self):
        nv = ""
        for n in self.nodes:
            nv += str(n) + "\n";
        return nv;

    def edgesAsString(self):
        res = "";
        for e in self.edges:
            res += str(e) + "\n";
        return res;

    def addNode(self, node):
        # Only add if node does not already exists
        for n in self.nodes:
            if (n.position == node.position):
                return;
        self.nodes.append(node);

    def addEdge(self, node1, node2, cost):
        for e in self.edges:
            if(Edge(node1, node2, cost) == e):
                return;
        self.edges.append(Edge(node1, node2, cost));

    def clearGraph(self):
        self.nodes = [];
        del self.edges[:];

    def djikstra(self):
        pass;

    def getNodesInCluster(self, clusterId):
        clusterNodes = [];

        for node in self.nodes:

            if node.clusterId == clusterId:
                print ("Adding")
                clusterNodes.append(node)
        print ("G getNodesInCluster: " + str(len(clusterNodes)))
        return clusterNodes
