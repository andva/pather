from graph import *
import random
from astar import AStar
WALL = 0;
FLOOR = 1;
PATH = 2;

TRANSITION_CONSTANT = 6;

ADD_EDGES_TO_MAP = True;

class Map:
    def __init__(self, width, height, nclusters):
        self.width = width;
        self.height = height;
        self.createBoard();
        self.createGraph();
        self.clusters = nclusters;
        self.cwidth = int(width / nclusters);
        self.cheight = int(height / nclusters);
        self.createEnt()
        self.intraClusterEdges(0)
    
    #Return status on board for given i (1D or 2D)
    def __getitem__(self,i):
        return self.board[self.getoffset(i)];

    def __setitem__(self,i,value):
        self.board[i] = value;

    #Converts board to string
    def __str__(self):
        v = "";
        for i in range(0, self.width * self.height):
            if(i % self.width == 0):
                v += str('\n')
                if(int(i / self.width) % self.cheight == 0):
                    v += str('\n')
            if(i % self.cwidth == 0):
                v += str('  ')
            if(self[i] == WALL):
                v += str('O')
            elif(self[i] == PATH):
                v += str(' ')
            else:
                v += str('M')
        return v;

    #Getter for 1D and 2D, used in getitem
    def getoffset(self,i):
        #If i is only one digit
        if(isinstance(i, (long, int))):
            return i;
        #if i is 2D
        if(len(i) > 2):
            raise IndexError
        return i[0] + i[1] * self.width;

    # Path between start and goal, only ok to walk in 
    # specified clusters.
    # Mode specifies if we want to return path or length
    def calculatePath(self, start, goal, clusterIds, mode):
        # Only length
        starSolver = AStar(self)
        starSolver.solveBetweenNodes(clusterIds, start, goal)
        if mode == 0:
            return 0;
        # Only path
        elif mode == 1:
            return [];

    def intraClusterEdges(self, clusterId):
        nodes = self.graph.getNodesInCluster(clusterId);
        # All nodes against all other nodes
        for i in xrange(0, len(nodes)):
            startNode = nodes[i];
            for j in xrange(i, len(nodes)):
                goalNode = nodes[j];
                # Find length between the nodes
                self.calculatePath(startNode, 
                    goalNode, [clusterId], 0);
                print("Done")
        
    #Fill board with random walls
    def createBoard(self):
        self.board = [FLOOR] * self.width * self.height;
        for x in range(1, self.width * 4):
            rid = random.randint(0, self.width * self.height-1);
            self.board[rid] = WALL;

    def createGraph(self):
        self.graph = Graph();
 
    def findEdge(self, clusterId, dirid):
        sizeId = 1;
        w =  self.clusters;
        edges = [-1, 0];
        wasLastFloor = False;
       #return empty list if border 
        if ((clusterId < w and dirid == 0) or
            ((clusterId * self.cwidth) % self.width == 0 and dirid == 1) or
            dirid > 1):
            return edges;
        else:
            #set up offsets
            if(dirid == 0):
                clusterLength = self.cwidth;
                offset = Position(0, -1);
                poffset = Position(1, 0);
                sp = Position(0,0);

            elif(dirid == 1):
                clusterLength = self.cheight;
                offset = Position(-1, 0);
                poffset = Position(0, 1);
                sp = Position(0,0);
            
            # Find world self position
            worldPosition = self.convertClusterv2Mapv(sp, clusterId);
            
            #Loop trough border of cluster.
            for j in range(0, clusterLength):
                #Get position in world of current brick
                p = worldPosition + Position(poffset.x * j, poffset.y * j);
                pairedPos = p + offset;

                # Compare tiles to see if current block-pair is entrance
                if((self[p.x, p.y] == FLOOR or self[p.x, p.y] == PATH) and
                        (self[pairedPos.x, pairedPos.y] == FLOOR or self[pairedPos.x, pairedPos.y] == PATH)):
                    # Found opening
                    wasLastFloor = True;
                    # Get indexes and add them to the list
                    mapIndex = self.convertMapv2Mapi(p);
                    mapIndex2 = self.convertMapv2Mapi(pairedPos);
                    edges.append(mapIndex);
                    edges.append(mapIndex2)
                    # Add to size count
                    edges[sizeId] += 1;
                else:
                    if(wasLastFloor):
                        edges.append(-1);
                        edges.append(0);
                        sizeId = len(edges) - 1;
                        wasLastFloor = False;
            return edges;

    def createNodeFromId(self, edgeId):
        if ADD_EDGES_TO_MAP:
            self[edgeId] = PATH;
        p = self.convertMapi2Mapv(edgeId);
        clusterId = self.convertMapv2ClusterId(p);
        return Node(p, clusterId);

    def parseEdgeList(self, edgeList):
        value = edgeList.pop(0);
        # If list is faulty
        if value != -1:
            return;
        # Get length of current edge
        size = edgeList.pop(0);
        edgeNum = size * 2;

        #If empty list
        if size == 0:
            return;
        # Decide if we want one or two entrances
        if size <= TRANSITION_CONSTANT:
            # Create one entrance in the middle
            if size % 2 != 0:
                middle = int(size / 2) * 2;
            else:
                middle = int(size);
            # Get id for entrance
            edgeId1 = edgeList[middle];
            edgeId2 = edgeList[middle + 1];
            # Create nodes
            n1 = self.createNodeFromId(edgeId1);
            n2 = self.createNodeFromId(edgeId2);
            # Add nodes and edges to graph 
            self.graph.addNode(n1);
            self.graph.addNode(n2);
            self.graph.addEdge(n1, n2, 1);
            for i in range(0, edgeNum):
                #Clear all edges in edgelist
                edgeList.pop(0);
        else:
            # Create two entrances in each edge
            edgeId = [];
            nodes = [];
            edgeId.append(edgeList[0]);
            edgeId.append(edgeList[1]);
            edgeId.append(edgeList[edgeNum-1]);
            edgeId.append(edgeList[edgeNum-2]);
            for i in range(0, 4):
                nodes.append(self.createNodeFromId(edgeId[i]));
                #   Add node to graph
                self.graph.addNode(nodes[i]);
            #Add edges, cost is 1 (they are next to each other)
            self.graph.addEdge(nodes[0], nodes[1], 1);
            self.graph.addEdge(nodes[2], nodes[3], 1);
            for i in range(0, edgeNum):
                #Clear all edges in edgelist
                edgeList.pop(0);

        # If edge have more parts
        v = edgeList[0] if edgeList else -2;
        if v == -1:
            self.parseEdgeList(edgeList);
        else:
            return;

    def createEnt(self):
        for i in range(0, self.clusters * self.clusters):
            for dirid in range(0, 2):
                edge = self.findEdge(i, dirid);
                # Edge list not empty
                if len(edge) > 2:
                    self.parseEdgeList(edge);

    def createSubMap(self, ptopleft, pbotright):
        submap = [];
        width = (pbotright.x - ptopleft.x);
        height = (pbotright.y - ptopleft.y);
        length = width * height;
        for i in range(0, length):
		x = ptopleft.x + i % width;
        y = ptopleft.y + int(i / width);
        globalId = self.convertMapv2Mapi(Position(x,y));
        submap.append(self[globalId]);

    def convertClusteri2Mapi(self, i, clusterid):
        p = self.convertClusteri2Mapv(i, clusterid);
        return self.convertMapv2Mapi(p); 
    
    def convertMapv2Mapi(self, p):
        return p.y * self.width + p.x;

    def convertMapi2Mapv(self, i):
        x = i % self.width;
        y = int(i / self.width);
        return Position(x, y);

    def convertClusterv2Mapi(self, p, clusterid):
        x = (clusterid % self.clusters) * self.cwidth + p.x;
        y = int(clusterid / self.clusters) * self.cheight + p.y;
        return self.convertMapv2Mapi(Position(x,y)); 
	
    def convertMapv2ClusterId(self, p):
        cx = int(p.x / self.cwidth);
        cy = int(p.y / self.cheight);
        cid = cy * self.clusters + cx
        return cid

    def convertClusteri2Mapv(self, i, clusterid):
        y = int(clusterid / self.clusters) * self.cheight;
        x = (clusterid % self.clusters) * self.cwidth;
        
        x += i % self.cwidth;
        y += int(i / self.cwidth);

        return Position(x,y);

    def convertClusterv2Mapv(self, p, clusterid):
        dirid = self.convertClusterv2Mapi(p, clusterid)
        return self.convertMapi2Mapv(dirid);

    def isPositionValid(self, p):
        return ( p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height);