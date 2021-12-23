
from .BlitMaster.blitmaster import layer

from . import constants


class Tile(object):

    REGISTRY = {}
    REMAINING = {k: set() for k in constants.DIGITS}

    def __init__(self, coord):
        (x, y) = coord
        assert (x + 1) in constants.DIGITS
        assert (y + 1) in constants.DIGITS
        self._coord = (x, y)
        self._row = y
        self._column = x
        self._box = Tile.to_box(x, y)

        self._value = None
        self._options = set(constants.DIGITS)

        Tile.REGISTRY[self.coord] = self
        self.register()

        self.layer = layer.Layer((7, 3))

    @staticmethod
    def get(coord):
        return Tile.REGISTRY[coord]

    @staticmethod
    def to_box(x, y):
        assert (x + 1) in constants.DIGITS
        assert (y + 1) in constants.DIGITS
        return (x // 3) + 3 * (y // 3)

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
        assert value in constants.DIGITS
        self.discard_options(constants.DIGITS - set([value]))

    def discard_down_to_options(self, keep):
        assert keep <= constants.DIGITS
        discard = constants.DIGITS - keep
        self.discard_options(discard)

    def discard_options(self, discard):
        assert discard <= constants.DIGITS  # <= vs < is for easier testing errors
        self.options -= discard

        if self.order == 1:
            self.value = list(self.options)[0]
        elif self.order == 0:
            raise ImpossibleTileError("Tile {} has no options left after removing {}!".format(self, discard))

    def render(self):
        if self.value is not None:
            lines = [
                "      ",
                "  [{}]  ".format(self.value),
                "      "
            ]
        else:
            lines = [
                " {} {} {} ".format(1 if 1 in self.options else ' ',
                                    2 if 2 in self.options else ' ',
                                    3 if 3 in self.options else ' '),
                " {} {} {} ".format(4 if 4 in self.options else ' ',
                                    5 if 5 in self.options else ' ',
                                    6 if 6 in self.options else ' '),
                " {} {} {} ".format(7 if 7 in self.options else ' ',
                                    8 if 8 in self.options else ' ',
                                    9 if 9 in self.options else ' ')
            ]

        self.layer.setlines(0, 0, lines)
        return self.layer.debug_render()

    def __repr__(self):
        return "<Tile {:x}: {}, {}, {}>".format(id(self), self.coord, self._value, self.options)

    def __hash__(self):
        return hash(self.coord)
