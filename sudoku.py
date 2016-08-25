
DIGITS = frozenset((1, 2, 3, 4, 5, 6, 7, 8, 9))


class Error(Exception): pass
class ImpossibleTileError(Error): pass


def ALL_DIGITS():
    return set(DIGITS)


class Tile(object):

    registry = {k: set() for k in DIGITS}

    def __init__(self, coord, value=None):
        self.coord = coord
        self.value = value
        self.options = ALL_DIGITS()
        self.add()
        if value is not None:
            self.discard_options(DIGITS - set([value]))

    def order(self):
        return len(self.options)

    def add(self):
        self.registry[self.order()].add(self)

    def remove(self):
        self.registry[self.order()].remove(self)

    def discard_options(self, discarded):
        self.remove()
        self.options -= discarded
        self.add()

        if len(self.options) == 1:
            self.value = list(self.options)[0]
        elif len(self.options) == 0:
            raise ImpossibleTileError("Tile {} has no options left after removing {}!".format(self, discarded))

    def __repr__(self):
        return "<Tile@{}: {}, {}, {}>".format(id(self), self.coord, self.value, self.options)

    def __hash__(self):
        return id(self)


T = Tile((3, 5), value=2)
print T
print Tile.registry
