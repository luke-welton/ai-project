from threes import Board
from threes import Directions

if __name__ == "__main__":
    start = Board()
    print("Start:\n{}".format(start))

    for direction in Directions:
        print("{}:\n{}".format(direction, Board(start, direction)))
