from threes import Board, Directions, Tile, InvalidMove
from copy import deepcopy


class TreeNode(object):
    def __init__(self, board, depth, value=0, direction=None):
        self.board = board
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
            sim_place_tile2(next_board, direction, search_depth, node)
        except InvalidMove:
            pass


# Simulates tile placement and value on all tree levels
def sim_place_tile(board, direction, search_depth, direction_node):
    if direction_node.depth + 1 == search_depth * 2:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction, x=x, y=y)
                        node = TreeNode(board_copy, direction_node.depth + 1, value=board_copy.calculate_score())
                        direction_node.add_child(node)
        return
    elif direction_node.depth == 1:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    next_tile = board.next_tile
                    board_copy = deepcopy(board)
                    board_copy.place_new_tile(next_tile, direction, x=x, y=y)
                    node = TreeNode(board_copy, direction_node.depth + 1)
                    direction_node.add_child(node)
                    sim_move(board_copy, search_depth, node)
    else:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    for i in range(1, 4):
                        board_copy = deepcopy(board)
                        board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction, x=x, y=y)
                        node = TreeNode(board_copy, direction_node.depth + 1)
                        direction_node.add_child(node)
                        sim_move(board_copy, search_depth, node)


# Simulates tile placement on first tree level and then only simulates tile value on future tree levels
# Much faster if search_depth > 2
def sim_place_tile2(board, direction, search_depth, direction_node):
    if direction_node.depth + 1 == search_depth * 2:
        for i in range(1, 4):
            board_copy = deepcopy(board)
            board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction)
            node = TreeNode(board_copy, direction_node.depth + 1, value=board_copy.calculate_score())
            direction_node.add_child(node)
        return
    elif direction_node.depth == 1:
        for x, row in enumerate(board.spaces):
            for y, space in enumerate(row):
                if space is None:
                    next_tile = board.next_tile
                    board_copy = deepcopy(board)
                    board_copy.place_new_tile(next_tile, direction, x=x, y=y)
                    node = TreeNode(board_copy, direction_node.depth + 1)
                    direction_node.add_child(node)
                    sim_move(board_copy, search_depth, node)
    else:
        for i in range(1, 4):
            board_copy = deepcopy(board)
            board_copy.place_new_tile(Tile(max_value=i, force_value=True), direction)
            node = TreeNode(board_copy, direction_node.depth + 1)
            direction_node.add_child(node)
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
    # print(board)
    while True:
        # Board will not accept a move if it does not combine tiles
        if not board.has_move():
            score = board.calculate_score()
            max_tile = board.get_max_tile()
            return [score, max_tile]
        tree_root = TreeNode(board, 0)
        sim_move(board, search_depth, tree_root)
        direction = pick_direction(tree_root)
        board = Board(prev=board, direction=direction)
        # print(board)


def run_expectimax(iterations, search_depth):
    score_sum = 0
    max_tile_sum = 0
    high_score = 0
    high_max_tile = 0
    for i in range(iterations):
        ret = expectimax(search_depth)
        score = ret[0]
        max_tile = ret[1]
        score_sum += score
        max_tile_sum += max_tile
        if score > high_score:
            high_score = score
        if max_tile > high_max_tile:
            high_max_tile = max_tile
        print("Score = " + str(score) + " Max Tile = " + str(max_tile))
    avg_score = score_sum / iterations
    avg_max_tile = max_tile_sum / iterations
    print("Average score with search depth of " + str(search_depth) + ": " + str(avg_score))
    print("Highest score with search depth of " + str(search_depth) + ": " + str(high_score))
    print("Average max tile with search depth of " + str(search_depth) + ": " + str(avg_max_tile))
    print("Highest max tile with search depth of " + str(search_depth) + ": " + str(high_max_tile))
    print("\n\n\n")
