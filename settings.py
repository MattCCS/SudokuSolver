
import os
import sys
assert sys.version_info >= (3, 4, 0)
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

BOARD_PATH = str(ROOT / "empty_board.txt")
BOX_PATH = str(ROOT / "empty_box.txt")
