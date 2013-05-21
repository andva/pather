from graph import *
import random

WALL = 0;
FLOOR = 1

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
        self.createEnt();

    def getoffset(self,i):
        if(isinstance(i, (long, int))):
            return i;
        if(len(i) > 2):
            raise IndexError
        return i[0] + i[1] * self.width;

    def __getitem__(self,i):
        return self.board[self.getoffset(i)];

    def __str__(self):
        v = "";
        for i in range(0, self.width * self.height):
            if(i % self.width == 0):
                v += str('\n')
                if(int(i / self.cwidth) % self.cheight == 0):
                    v+= str('\n')
            if(i % self.cwidth == 0):
                v += str('  ')
            if(self[i] == WALL):
                v += str('O')
            else:
                v += str('M')
        return v;

    def createBoard(self):
        self.board = [FLOOR] * self.width * self.height;
        for x in range(1, self.width * 2):
            id = random.randint(0, self.width * self.height-1);
            self.board[id] = WALL;

    def createGraph(self):
        self.graph = Graph();
 
    def findEdge(self, clusterId, dir):
        id = 0;
        w =  self.clusters;
        h = w;
        edges = [];
        edges.append([]);
        wasLastFloor = False;
        
        if ((clusterId < w and dir == 0) or
            (clusterId % w != w - 1 and dir == 1) or
            dir > 1):
            return edges;
        else:
            if(dir == 0):
                clusterLength = self.cwidth;
                offset = Position(0, -1);
                poffset = Position(1, 0);
            elif(dir == 1):
                clusterLength = self.cheight;
                offset = Position(-1, 0);
                poffset = Position(0, 1);
            localP = Position(0,0);

            for j in range(0, clusterLength):
                
                p = self.convertClusteri2Mapv(j, clusterId);
                if(self[p.x, p.y] == FLOOR and
                        self[(p + offset).x, (p + offset).y] == FLOOR):
                    wasLastFloor = True;
                    if not edges:
                        raise Exception("error");
                    if not edges[id]:
                    #if not edges[id]:
                        edges[id] = [0];
                        edges[id].append(self.convertMapv2Mapi(p));

                    edges[id][0] += 1;
                    if j == clusterLength - 1:
                        edges[id].append(self.convertMapv2Mapi(p));
                else:
                    if(wasLastFloor):
                        edges[id].append(self.convertMapv2Mapi(p + offset));
                        id += 1;
                        wasLastFloor = False;
            return edges;

    def createEnt(self):
        for i in range(0, self.clusters * self.clusters):
            for dir in range(0, 2):
                edge = self.findEdge(i, dir);
                print "D:",
                print dir,
                print " E:",
                print edge;

    def createEntrances(self):
        w =  self.clusters;
        h = w;
#each borderline                
        for i in range(0, self.clusters * self.clusters):
            id = 0;
            edges = [];
            edges.append([]);
            wasLastFloor = False;
            for j in range(0, self.cwidth):
                if(i >= w):
                    p = self.convertClusteri2Mapv(j, i);
                    if(self[p.x,p.y] == FLOOR 
                            and self[p.x, p.y - 1] == FLOOR):
                        wasLastFloor = True;
                        if not edges[id]:
                            edges[id].append(0);
                            edges[id].append(self.convertClusteri2Mapi(j,i));
                        edges[id][0] += 1;
                        if j == self.cwidth - 1:
                            edges[id].append(self.convertClusteri2Mapi(j,i));
                    else:
                        if(wasLastFloor):
                            edges[id].append(self.convertClusteri2Mapi(j,i) - 1);
                            id += 1;
                            wasLastFloor = False;
                if(i < (h) * (w - 1)):
                    pass;
            print "min: ",
            print min(edges);
            for m in edges:
                print len(m)
            for i in range(0, self.cheight):
                if(i % w != w - 1):
                    pass;
                if(i % w != 0):
                    pass;

    def convertClusteri2Mapi(self, i, clusterid):
        p = self.convertClusteri2Mapv(i, clusterid);
        return self.convertMapv2Mapi(p); 
    
    def convertMapv2Mapi(self, p):
        print p;
        return p.y * self.width * p.x;

    def convertClusterv2Mapi(self, p, clusterid):
        print "P:",
        print p,
        print " nP:",

        y = int(clusterid / self.clusters) * self.cheight + p.y;
        x = (clusterid % self.clusters) * self.cwidth + p.x;
        print Position(x,y);
        return self.convertMapv2Mapi(p); 
        

    def convertClusteri2Mapv(self, i, clusterid):
        y = int(clusterid / self.clusters) * self.cheight;
        x = (clusterid % self.clusters) * self.cwidth;
        
        x += i % self.cwidth;
        y += int(i / self.cwidth);

        return Position(x,y);

    def convertClusterv2Mapv(self, x, y, clusterid):
        raise Exception("Not implemented.");

class Cluster:
    def __init__(self):
        pass;
