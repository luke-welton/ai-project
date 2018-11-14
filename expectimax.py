from threes import Board, Directions, Tile, InvalidMove
from copy import deepcopy


class TreeNode(object):
    def __init__(self, data, depth, value=0, direction = None):
        self.data = data
        self.value = value
        self.depth = depth
        self.children = []
        self.direction = direction

    def add_child(self, obj):
        self.children.append(obj)

    def remove_child(self, obj):
        self.children.remove(obj)


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
    if direction_node.depth + 1 == search_depth * 2:
        for row in board.spaces:
            for space in row:
                if space is not None:
                    continue
                else:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        board_copy.place_new_tile(Tile(3, force_value=i), direction)
                        node = TreeNode(board_copy, direction_node.depth + 1, value=board_copy.calculate_score())
                        direction_node.add_child(node)
                        # print("Depth = " + str(node.depth) + " Tile Value = " + str(i))
        return
    else:
        for row in board.spaces:
            for space in row:
                if space is not None:
                    continue
                elif direction_node.depth == 2:
                    next_tile = board.next_tile
                    board_copy = deepcopy(board)
                    # need to be able to force location too
                    board_copy.place_new_tile(next_tile, direction)
                    node = TreeNode(board_copy, direction_node.depth + 1)
                    direction_node.add_child(node)
                    # print("Depth = " + str(node.depth) + " Tile Value = " + str(next_tile.value))
                    sim_move(board_copy, search_depth, node)
                else:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        # need to be able to force location too
                        board_copy.place_new_tile(Tile(3, force_value=i), direction)
                        node = TreeNode(board_copy, direction_node.depth + 1)
                        direction_node.add_child(node)
                        # print("Depth = " + str(node.depth) + " Tile Value = " + str(i))
                        sim_move(board_copy, search_depth, node)
    return


def pick_direction(tree):
    best_direction = None
    best_value = 0
    for direction in tree.children:
        direction_value = calculate_averages(direction)
        # print(direction_value)
        if direction_value > best_value:
            best_value = direction_value
            best_direction = direction.direction
    return best_direction


def calculate_averages(node):
    if len(node.children) == 0:
        return node.value
    children_sum = 0
    for child in node.children:
        children_sum += calculate_averages(child)
    return children_sum / len(node.children)


def expectimax(search_depth):
    board = Board()
    print(board)
    moves = 0
    while moves < 30:
        if not board.has_move():
            return board
        tree_root = TreeNode(board, 0)
        sim_move(board, search_depth, tree_root)
        direction = pick_direction(tree_root)
        board = Board(prev=board, direction=direction)
        print(board)
        moves += 1
    return 0



# def sim_move_tiles(board, depth):
#     score = board.calculate_score()
#     if depth <= 0:
#         print(board)
#         return score
#     depth -= 1
#     best_move_value = 0
#     for direction in Directions:
#         try:
#             next_board = Board(prev=board, direction=direction)
#             move_value = sim_place_tile(next_board, depth)
#             if move_value >= best_move_value:
#                 best_move_value = move_value
#                 best_move_board = next_board
#         except InvalidMove:
#             pass
#     return best_move_value
#
#
# def sim_place_tile(board, depth):
#     score = 0
#     for row in board.spaces:
#         for space in row:
#             if space is None:
#                 continue
#             else:
#                 for i in range(1, 4):
#                     board_copy = deepcopy(board)
#                     board_copy.place_tile_no_move(Tile(3, force_value=i))
#                     score += sim_move_tiles(board_copy, depth)
#     return score / 3

