
import textwrap

from .BlitMaster.blitmaster import layer

from . import constants
from . import coords
from . import settings
from .tile import Tile


with open(settings.BOARD_PATH) as empty_board:
    EMPTY_BOARD = empty_board.read().strip().split('\n')

with open(settings.BOX_PATH) as empty_box:
    EMPTY_BOX = empty_box.read().strip().split('\n')


def chunk(s, size=9):
    return textwrap.wrap(s, size)


def iterate_board(board):
    board = chunk(board.strip().replace(' ', '').replace('\n', ''))

    print("Loading...")
    assert len(board) == len(constants.DIGITS)
    for (y, row) in enumerate(board):
        print(' '.join(row))
        assert len(row) == len(constants.DIGITS)
        for (x, val) in enumerate(row):
            coord = (x, y)
            if val.isdigit():
                val = int(val)
                assert val in constants.DIGITS
            else:
                val = None

            yield (coord, val)


class Board(object):

    ROWS = {k: set() for k in range(9)}
    COLUMNS = {k: set() for k in range(9)}
    BOXES = {k: set() for k in range(9)}

    def __init__(self, board=None):
        self.layer = layer.Layer((77, 39))
        self.boxes = [layer.Layer((25, 13)) for _ in range(9)]

        # create tiles
        if board is not None:
            for (coord, val) in iterate_board(board):
                self.create_tile(coord, val)

        # set up layers
        for (i, (rbx, rby)) in enumerate(coords.generate_2d(3, 3)):
            box_layer = self.boxes[i]
            box_layer.setlines(0, 0, EMPTY_BOX)

            (bx, by) = (rbx, rby)
            (gbx, gby) = (bx * 26, by * 13)
            self.layer.add_layer(gbx, gby, box_layer)

            for (rtx, rty) in coords.generate_2d(3, 3):
                (tx, ty) = (bx * 3 + rtx, by * 3 + rty)
                (gtx, gty) = (rtx * 8 + 1, rty * 4 + 1)

                tile_layer = Tile.get((tx, ty)).layer
                box_layer.add_layer(gtx, gty, tile_layer)

    def create_tile(self, coord, val=None):
        tile = Tile(coord)
        if val is not None:
            tile.set(val)

        self.add_tile(tile)

    def add_tile(self, tile):
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

    def render(self):
        for (_, tile) in Tile.REGISTRY.items():
            tile.render()

        return self.layer.debug_render()

    def __iter__(self):
        return iter(Tile.get(coord) for coord in coords.generate_2d(9, 9))

    def groups(self):
        for (name, group) in (("row", Board.ROWS), ("column", Board.COLUMNS), ("box", Board.BOXES)):
            for (num, cut) in sorted(group.items()):
                yield (name, num, cut)

    def is_solved(self):
        return all(t.value for t in self)
