import random
from math import log2
from copy import deepcopy
from enum import Enum


class InvalidTileValue(Exception):
    pass


class InvalidDirection(Exception):
    pass


class InvalidMove(Exception):
    pass


class InvalidTilePlacement(Exception):
    pass


# checks whether or not a value is valid for a tile
def is_valid(value):
    if value == 1 or value == 2:
        return True

    value /= 3
    while value > 1:
        if value % 2 != 0:
            return False
        else:
            value /= 2

    return True


class Tile:
    def __init__(self, max_value, force_value=False):
        self.value = 0

        if force_value:
            self.value = max_value
        else:
            r = random.random()

            if r > 2/3:
                self.value = 2
            elif r > 1/3:
                self.value = 1
            else:
                self_max = max_value / 2
                num_vals = int(log2(self_max / 3))
                divisor = 2 ** num_vals - 1  # sum of 2^n for all n < num_vals

                for i in range(num_vals):
                    if r < (2 ** i) / divisor * 1/3:
                        self.value = 3 * 2 ** (num_vals - i)
                        break

                # if the value should be 3, then it will currently be 0
                if self.value == 0:
                    self.value = 3

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def merge(self, to_merge):
        self.value += to_merge.value

        if not is_valid(self.value):
            raise InvalidTileValue("The value of the tile was not 1, 2, or 3(2)^n for any n.")

    def can_combine(self, other):
        if self.value == 1 and other.value == 2:
            return True
        if self.value == 2 and other.value == 1:
            return True
        if self.value > 2 and self.value == other.value:
            return True
        return False


class Directions(Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class Board:
    def __init__(self, prev=None, direction=-1, add_tile=True):
        if prev is None:
            self.max_value = 3
            self.spaces = []
            self.next_tile = Tile(self.max_value)
            for _ in range(4):
                arr = []
                for _ in range(4):
                    arr.append(None)
                self.spaces.append(arr)

            # populate board with tiles
            num_tiles = 0
            while num_tiles < 9:
                x = random.randint(0, len(self.spaces) - 1)
                y = random.randint(0, len(self.spaces[len(self.spaces) - 1]) - 1)

                if self.spaces[x][y] is None:
                    self.spaces[x][y] = Tile(self.max_value)
                    num_tiles += 1
        else:
            self.max_value = prev.max_value
            self.spaces = deepcopy(prev.spaces)
            self.calculate_tiles(direction)
            self.next_tile = None

            if self == prev:
                raise InvalidMove(
                    "The generated board was not different from the previous board.\n" + str(prev) + "\n" + str(self))
            elif add_tile:
                self.place_new_tile(prev.next_tile, direction)

        # self.next_tile = Tile(self.max_value)
        self.score = self.calculate_score()

    def __eq__(self, other):
        try:
            for i in range(len(self.spaces)):
                for j in range(len(self.spaces[i])):
                    if self.spaces[i][j].value != other.spaces[i][j].value:
                        return False
            return True
        except (AttributeError, IndexError):
            return False

    def __str__(self):
        output = ""
        for row in self.spaces:
            for cell in row:
                if cell is None:
                    value = 0
                else:
                    value = cell.value

                output += "{}\t".format(value)
            output += "\n"
        return output

    # function to calculate the new tiles after making a move
    # this function could pretty easily be condensed but it'd be a hell of a lot less readable
    def calculate_tiles(self, direction):
        if direction == Directions.down:
            for i in range(len(self.spaces) - 1):
                # we want to check from the bottom upward
                i = len(self.spaces) - i - 2

                for j in range(len(self.spaces[i])):
                    upper = self.spaces[i][j]
                    lower = self.spaces[i + 1][j]

                    if upper is None:
                        continue
                    elif lower is None:
                        self.spaces[i + 1][j] = upper
                        self.spaces[i][j] = None
                    elif upper == lower and upper.value >= 3 \
                            or upper.value == 1 and lower.value == 2 \
                            or lower.value == 1 and upper.value == 2:
                        lower.merge(upper)
                        self.spaces[i][j] = None

                        if lower.value > self.max_value:
                            self.max_value = lower.value

        elif direction == Directions.right:
            for i in range(len(self.spaces)):
                for j in range(len(self.spaces[i]) - 1):
                    # we want to check from the right to the left
                    j = len(self.spaces[i]) - j - 2

                    left = self.spaces[i][j]
                    right = self.spaces[i][j + 1]

                    if left is None:
                        continue
                    elif right is None:
                        self.spaces[i][j + 1] = left
                        self.spaces[i][j] = None
                    elif left == right and left.value >= 3 \
                            or left.value == 1 and right.value == 2 \
                            or right.value == 1 and left.value == 2:
                        right.merge(left)
                        self.spaces[i][j] = None

                        if right.value > self.max_value:
                            self.max_value = right.value

        elif direction == Directions.up:
            for i in range(1, len(self.spaces)):
                for j in range(len(self.spaces[i])):
                    upper = self.spaces[i - 1][j]
                    lower = self.spaces[i][j]

                    if lower is None:
                        continue
                    elif upper is None:
                        self.spaces[i - 1][j] = lower
                        self.spaces[i][j] = None
                    elif upper == lower and upper.value >= 3 \
                            or upper.value == 1 and lower.value == 2 \
                            or lower.value == 1 and upper.value == 2:
                        upper.merge(lower)
                        self.spaces[i][j] = None

                        if upper.value > self.max_value:
                            self.max_value = upper.value

        elif direction == Directions.left:
            for i in range(len(self.spaces)):
                for j in range(1, len(self.spaces[i])):
                    left = self.spaces[i][j - 1]
                    right = self.spaces[i][j]

                    if right is None:
                        continue
                    elif left is None:
                        self.spaces[i][j - 1] = right
                        self.spaces[i][j] = None
                    elif left == right and left.value >= 3 \
                            or left.value == 1 and right.value == 2 \
                            or right.value == 1 and left.value == 2:
                        left.merge(right)
                        self.spaces[i][j] = None

                        if left.value > self.max_value:
                            self.max_value = left.value
        else:
            raise InvalidDirection(
                "An invalid integer was passed to the Board constructor for direction." + str(direction))

    # places a tile randomly on the board
    def place_new_tile(self, new_tile, direction, x=-1, y=-1):
        if x > -1 and y > -1:
            if self.spaces[x][y] is None:
                self.spaces[x][y] = new_tile
                self.score = self.calculate_score()
                self.next_tile = Tile(self.max_value)
            else:
                raise InvalidTilePlacement("A tile was placed in a spot that already had a tile.")
        else:
            placed = False
            while not placed:
                x = y = -1
                if direction == Directions.up:
                    x = len(self.spaces) - 1
                elif direction == Directions.right:
                    y = 0
                elif direction == Directions.down:
                    x = 0
                elif direction == Directions.left:
                    y = len(self.spaces[len(self.spaces) - 1]) - 1

                if x < 0:
                    x = random.randint(0, len(self.spaces) - 1)
                if y < 0:
                    y = random.randint(0, len(self.spaces[len(self.spaces) - 1]) - 1)

                if self.spaces[x][y] is None:
                    self.spaces[x][y] = new_tile
                    placed = True
                    self.score = self.calculate_score()
                    self.next_tile = Tile(self.max_value)

    def has_move(self):
        for direction in Directions:
            try:
                board_copy = deepcopy(self)
                Board(board_copy, direction)
                return True
            except InvalidMove:
                pass
        return False

    def calculate_score(self):
        score = 0
        for row in self.spaces:
            for cell in row:
                if cell is not None and cell.value >= 3:
                    score += 3 ** (log2(cell.value / 3) + 1)

        return int(score)

    def get_max_tile(self):
        max_tile = 0
        for row in self.spaces:
            for cell in row:
                if cell is not None and cell.value > max_tile:
                    max_tile = cell.value
        return max_tile

    @staticmethod
    def tile_man_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    # New heuristic did not make as much of a difference as search depth, so we just used the score as our heuristic to
    # increase efficiency
    def calculate_reward(self):
        score = self.calculate_score()
        # tile_closeness = 0
        # open_spaces = 0
        #
        # for x1, row1 in enumerate(self.spaces):
        #     for y1, cell1 in enumerate(row1):
        #         if cell1 is None:
        #             open_spaces += 1
        #             continue
        #         for x2, row2 in enumerate(self.spaces):
        #             for y2, cell2 in enumerate(row2):
        #                 if cell2 is None:
        #                     continue
        #                 if cell1.can_combine(cell2):
        #                     man_dist = Board.tile_man_distance(x1, y1, x2, y2)
        #                     if 0 < man_dist < 3:
        #                         # print(reward)
        #                         logmax = int(log2(self.max_value / 3) + 1)
        #                         if cell1.can_combine(cell2):
        #                             tile_closeness += man_dist * int(logmax - log2(cell1.value / 3) - 1)
        #                         elif cell1.value != cell2.value:
        #                             tile_closeness += man_dist * logmax
        #
        # reward = (0.1 * tile_closeness) + score
        return score
