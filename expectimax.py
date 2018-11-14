from threes import Board, Directions, Tile, InvalidMove
from copy import deepcopy


class TreeNode(object):
    def __init__(self, data, depth, value=0, direction=None):
        self.data = data
        self.value = value
        self.depth = depth
        self.children = []
        self.direction = direction

    def add_child(self, obj):
        self.children.append(obj)

    def remove_child(self, obj):
        self.children.remove(obj)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


def sim_move(board, search_depth, tile_node):
    for direction in Directions:
        try:
            next_board = Board(prev=board, direction=direction, add_tile=False)
            node = TreeNode(next_board, tile_node.depth + 1, direction=direction)
            tile_node.add_child(node)
            # print("Depth = " + str(node.depth) + " Direction = " + str(direction))
            sim_place_tile(board, direction, search_depth, node)
        except InvalidMove:
            pass


def sim_place_tile(board, direction, search_depth, direction_node):
    if direction_node.depth == 1:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    next_tile = board.next_tile
                    board_copy = deepcopy(board)
                    board_copy.place_new_tile(next_tile, direction, x=x, y=y)
                    node = TreeNode(board_copy, direction_node.depth + 1)
                    direction_node.add_child(node)
                    # print("Depth = " + str(node.depth) + " Tile Value = " + str(next_tile.value))
                    sim_move(board_copy, search_depth, node)

    elif direction_node.depth + 1 == search_depth * 2:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction, x=x, y=y)
                        node = TreeNode(board_copy, direction_node.depth + 1, value=board_copy.calculate_score())
                        direction_node.add_child(node)
                        # print("Depth = " + str(node.depth) + " Tile Value = " + str(i))
        return
    else:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        # need to be able to force location too
                        board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction, x=x, y=y)
                        node = TreeNode(board_copy, direction_node.depth + 1)
                        direction_node.add_child(node)
                        # print("Depth = " + str(node.depth) + " Tile Value = " + str(i))
                        sim_move(board_copy, search_depth, node)


def calculate_average(node):
    if len(node.children) == 0:
        return node.value
    children_sum = 0
    for child in node.children:
        children_sum += calculate_average(child)
    average_child = children_sum / (len(node.children))
    node.value = average_child
    return average_child


def pick_direction(tree):
    best_direction = tree.children[0].direction
    best_value = 0
    for direction in tree.children:
        direction_value = calculate_average(direction)
        direction.value = direction_value
        if direction_value > best_value:
            best_value = direction_value
            best_direction = direction.direction
    return best_direction


def expectimax(search_depth):
    board = Board()
    print(board)
    moves = 0
    while moves < 1000:
        # Board will not accept a move if it does not combine tiles
        if not board.has_move():
            return board
        tree_root = TreeNode(board, 0)
        sim_move(board, search_depth, tree_root)
        direction = pick_direction(tree_root)
        board = Board(prev=board, direction=direction)
        print(board)
        moves += 1
    return 0
