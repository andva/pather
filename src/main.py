# Implementation of near-optimal hierarchical pathfinding

from map import *

W = 12;
H = 12;

def main():
    _map = Map(W, H, 3);
    _map.createEnt();
    print _map;
    return

if __name__ == "__main__":
    main()
