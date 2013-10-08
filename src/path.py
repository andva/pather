from map import Position


class Path:
    def __init__(self, array=None):
        # Make sure that the path is a list
        if array is not None:
            assert isinstance(array, (list, tuple))
            assert not isinstance(array, basestring)
            self.array = array
        else:
            self.array = []

    def __str__(self):
        s = "Player path:"
        for position in self.array:
            s += " " + str(position)
        return s

    def __len__(self):
        if self.array is None:
            return 0
        return len(self.array)

    def addPosition(self, position):
        assert isinstance(position, Position)
        self.array.append(position)

    def popNextPosition(self):
        if len(self.array) > 0:
            return self.array.pop(0)
        else:
            return None