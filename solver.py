
import itertools


SHOW_LIVE = True


def explain_hidden_single(tile, name, num, value):
    print(f"[+] Because tile {tile} is the only tile in {name} {num} "
          f"with the value {value}, it *must* have that value!")


def explain_hidden_doubles(t1, t2, name, num, v1, v2):
    print(f"[+] Because tiles {t1} and {t2} are the only tiles in {name} {num} "
          f"with the values {v1} and {v2}, they cannot have any other values!")


def nCr(elements, n):
    for subset in itertools.combinations(elements, n):
        subset = set(subset)
        yield (subset, elements - subset)


def options(tiles):
    return set().union(*(t.options for t in tiles))


def get(set_):
    assert len(set_) == 1
    return list(set_)[0]


class Solver(object):

    def __init__(self, board, manual=False):
        self.board = board
        self.manual = manual

        self.show()
        print("^ the initial board\n")
        if self.manual:
            input("The initial board...")

        self.update_board()
        self.show()
        print("^ the first board\n")
        if self.manual:
            input("Begin?")

    def show(self):
        if SHOW_LIVE:
            print(self.board.render())

    def update_board(self):
        """Propagates final tile values"""
        for tile in self.board:
            if tile.value is not None:
                values = frozenset([tile.value])
                neighbors = self.board.neighbors_tile(tile)
                for ntile in neighbors:
                    ntile.discard_options(values)
                    ntile.render()

    def solve(self):
        print("Solving...")
        while self.solve_round():
            print()

            if self.manual:
                input("Continue?")

            self.update_board()
            self.show()
            if self.manual and SHOW_LIVE:
                input("Continue?")

            solved = self.board.is_solved()
            if solved:
                break

        if solved:
            print("~~~ SOLVED! ~~~")
        else:
            print("[-] Could not solve.")

        return solved

    def solve_round(self):
        """Returns whether any progress was made"""
        steps = [
            self.check_hidden_singles,
            self.check_hidden_doubles,
        ]

        for step in steps:
            if step():
                return True

        return False

    def check_hidden_singles(self):
        print("Checking hidden singles...")
        for (name, num, cut) in self.board.groups():
            for ((tile,), rest) in nCr(cut, 1):
                if tile.value:
                    continue

                unique = tile.options - options(rest)
                if len(unique) == 1:
                    value = get(unique)
                    explain_hidden_single(tile, name, num, value)
                    tile.set(value)
                    return True

    def check_hidden_doubles(self):
        print("Checking hidden doubles...")
        for (name, num, cut) in self.board.groups():
            for ((t1, t2), rest) in nCr(cut, 2):
                if t1.value or t2.value:
                    continue

                unique = (t1.options & t2.options) - options(rest)
                if t1.options == t2.options == unique:
                    continue

                if len(unique) == 0:
                    continue
                elif len(unique) > 2:
                    exit(f"[!] (Hidden Double) Tiles {t1} and {t2} in "
                         f"{name} {num} share {unique}, which will not resolve!")
                elif len(unique) == 2:
                    t1.discard_down_to_options(unique)
                    t2.discard_down_to_options(unique)
                    (v1, v2) = list(unique)
                    explain_hidden_doubles(t1, t2, name, num, v1, v2)
                    return True
                    # check locked candidates ...
                else:
                    pass
                    # check locked candidates ...
