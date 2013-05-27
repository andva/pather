from graph import *
import random

WALL = 0;
FLOOR = 1;
PATH = 2;

TRANSITION_CONSTANT = 6;

class Map:
    def __init__(self, width, height, nclusters):
        self.width = width;
        self.height = height;
        self.createBoard();
        self.createGraph();
        self.clusters = nclusters;
        self.cwidth = int(width / nclusters);
        self.cheight = int(height / nclusters);
        #self.createEntrances();
        #self.createEnt();

#Getter for 1D and 2D, used in getitem
    def getoffset(self,i):
        #If i is only one digit
        if(isinstance(i, (long, int))):
            return i;
        #if i is 2D
        if(len(i) > 2):
            raise IndexError
        return i[0] + i[1] * self.width;

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
                v += str('E')
            else:
                v += str('M')
        return v;

#Fill board with random walls
    def createBoard(self):
        self.board = [FLOOR] * self.width * self.height;
        for x in range(1, self.width * 2):
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
                if(self[p.x, p.y] == FLOOR and
                        self[pairedPos.x, pairedPos.y] == FLOOR):
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
            self[edgeId1] = PATH;
            self[edgeId2] = PATH;
            p1 = self.convertMapi2Mapv(edgeId1);
           # n1 = Node(p1.x, p1.y, )
        else:
            # Create two entrances in each edge
            edgePair1 = Position(edgeList[0], edgeList[1]);
            edgePair2 = Position(edgeList[edgeNum-1], edgeList[edgeNum-2]);
            self[edgePair1.x] = PATH;
            self[edgePair1.y] = PATH;
            self[edgePair2.x] = PATH;
            self[edgePair2.y] = PATH;
        for i in range(0, edgeNum):
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

   # def mapP2

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
        

    def convertClusteri2Mapv(self, i, clusterid):
        y = int(clusterid / self.clusters) * self.cheight;
        x = (clusterid % self.clusters) * self.cwidth;
        
        x += i % self.cwidth;
        y += int(i / self.cwidth);

        return Position(x,y);

    def convertClusterv2Mapv(self, p, clusterid):
        dirid = self.convertClusterv2Mapi(p, clusterid)
        return self.convertMapi2Mapv(dirid);
