from map import Position

class Path:
    def __init__(self, path = None):
        # Make sure that the path is a list
        if path is not None:
            assert isinstance(path, (list, tuple))
            assert not isinstance(path, basestring)
        self.path = path

    def __str__(self):
        s = "Player path:"
        for i in self.path:
            s += " " + self.path[i]

    def addPosition(self, position):
        assert isinstance(position, Position)

    def popNextPosition(self):
        if len(self.path) > 0:
            return self.path.pop(0)
        else:
            return None


