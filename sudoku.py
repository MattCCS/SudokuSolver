
DIGITS = frozenset((1, 2, 3, 4, 5, 6, 7, 8, 9))

TEST_BOARD = """\
. . 6 . . 7 3 . .
. 1 8 . . 9 . 5 .
5 . . . . . . 6 4
9 2 . . 8 . . . .
. . . 7 6 3 . . .
. . . . 9 . . 7 5
6 3 . . . . . . 8
. 9 . 3 . . 5 2 .
. . 2 4 . . 6 . ."""

class Error(Exception): pass
class ImpossibleTileError(Error): pass


def ALL_DIGITS():
    return set(DIGITS)


def iterate_board(board):
    board = board.strip().replace(' ', '').split()
    print "Loading..."
    assert len(board) == len(DIGITS)
    for (y, row) in enumerate(board, 1):
        print ' '.join(row)
        assert len(row) == len(DIGITS)
        for (x, val) in enumerate(row, 1):
            coord = (x, y)
            if val.isdigit():
                val = int(val)
                assert val in DIGITS
            else:
                val = None

            yield (val, coord)


class Board(object):

    ROWS = {k: set() for k in DIGITS}
    COLUMNS = {k: set() for k in DIGITS}
    BOXES = {k: set() for k in DIGITS}

    def __init__(self):
        for (val, coord) in iterate_board(TEST_BOARD):
            self.setup_tile(val, coord)

    def setup_tile(self, val, coord):
        tile = Tile(coord)
        if val is not None:
            tile.set(val)

        Board.ROWS[tile.row].add(tile)
        Board.COLUMNS[tile.column].add(tile)
        Board.BOXES[tile.box].add(tile)

    def neighbors(self, coord):
        return self.neighbors_tile(Tile.get(coord))

    def neighbors_tile(self, tile):
        return self.neighbors_row(tile) | \
            self.neighbors_column(tile) | \
            self.neighbors_box(tile)

    def neighbors_row(self, tile):
        return Board.ROWS[tile.row] - set([tile])

    def neighbors_column(self, tile):
        return Board.COLUMNS[tile.column] - set([tile])

    def neighbors_box(self, tile):
        return Board.BOXES[tile.box] - set([tile])


class Tile(object):

    REGISTRY = {}
    REMAINING = {k: set() for k in DIGITS}

    def __init__(self, coord):
        (x, y) = coord
        assert x in DIGITS
        assert y in DIGITS
        self._coord = (x, y)
        self._row = y
        self._column = x
        self._box = Tile.to_box(x, y)

        self._value = None
        self._options = ALL_DIGITS()

        Tile.REGISTRY[self.coord] = self
        self.register()

    @staticmethod
    def get(coord):
        return Tile.REGISTRY[coord]

    @staticmethod
    def to_box(x, y):
        assert x in DIGITS
        assert y in DIGITS
        return ((x - 1) / 3) + 3 * ((y - 1) / 3) + 1

    @property
    def coord(self):
        return self._coord

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def box(self):
        return self._box

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value

    value = property(get_value, set_value)

    def get_options(self):
        return set(self._options)

    def set_options(self, new_options):
        self.unregister()
        self._options = new_options
        self.register()

    options = property(get_options, set_options)

    @property
    def order(self):
        return len(self.options)

    def register(self):
        Tile.REMAINING[self.order].add(self)

    def unregister(self):
        Tile.REMAINING[self.order].remove(self)

    def set(self, value):
        """Shorthand method to help on startup"""
        assert value in DIGITS
        self.discard_options(DIGITS - set([value]))

    def discard_options(self, discarded):
        assert discarded <= DIGITS  # <= vs < is for easier testing errors
        self.options -= discarded

        if self.order == 1:
            self.value = list(self.options)[0]
        elif self.order == 0:
            raise ImpossibleTileError("Tile {} has no options left after removing {}!".format(self, discarded))

    def __repr__(self):
        return "<Tile {:x}: {}, {}, {}>".format(id(self), self.coord, self._value, self.options)

    def __hash__(self):
        return id(self)


T = Tile((3, 5))
print T
print; print Board.ROWS
print; print Board.COLUMNS
print; print Board.BOXES
print; print Tile.REMAINING
T.discard_options(set([1,2,9]))
print; print T
print; print Tile.REMAINING

B = Board()
