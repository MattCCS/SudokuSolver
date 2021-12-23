
import argparse

from . import board
from . import constants
from . import solver


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("board", nargs="?")
    parser.add_argument("-m", "--manual", default=False, action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.board:
        main_board = board.Board(constants.TEST_BOARD)
    else:
        main_board = board.Board(args.board)

    # print(tile.Tile.get((1, 1)).render())
    # print(tile.Tile.get((2, 2)).render())
    # print(main_board.render())

    s = solver.Solver(main_board, manual=args.manual)
    s.solve()


if __name__ == '__main__':
    main()
