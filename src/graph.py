class Position:
        def __init__(self, x, y):
                self.x = x;
                self.y = y;

class Node:
        def __init__(self, x, y, id):
                self.position = Position(x, y);
                self.id = id;

class Graph:
        def __init__(self):
                self.nodes = [];
                self.edges = [];

        def addNode(self, position):
                self.nodes.append(position);

        def addEdge(self, node1, node2):
                print("hej!");
