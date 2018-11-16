from threes import Board, Directions, Tile, InvalidMove
from math import sqrt, log2


class Node:
    def __init__(self, board, prev=None):
        self.board = board
        self.next = []
        self.prev = prev

        self.move_count = 1
        if prev is not None:
            self.move_count += prev.move_count

        self.h = MAX_SCORE - self.board.calculate_score() + self.calculate_manhattan()

    def calculate_manhattan(self):
        distance = 0

        for i in range(len(self.board.spaces)):
            for j in range(len(self.board.spaces[i])):
                for x in range(i):
                    for y in range(j):
                        try:
                            a = self.board.spaces[i][j].value
                            b = self.board.spaces[x][y].value

                            if a == b and a >= 3 \
                                    or a == 1 and b == 2 \
                                    or a == 2 and b == 1:
                                manhattan = sqrt((i - x) ** 2 + (j - y) ** 2)

                                # we want to give preference to higher values, so multiply by logmax - log(value)
                                logmax = int(log2(self.board.max_value / 3) + 1)
                                if a == b:
                                    distance += manhattan * int(logmax - log2(a / 3) - 1)
                                else:
                                    distance += manhattan * logmax
                        except AttributeError:
                            continue

        return distance

    def generate_next(self):
        for direction in Directions:
            try:
                self.next.append(Node(Board(self.board, direction), self))
            except InvalidMove:
                continue

    def update_node(self, new_node):
        self.prev = new_node.prev
        self.move_count = new_node.move_count


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        index = -1
        for i in range(len(self)):
            if index < 0 or self.queue[i].h < self.queue[index].h:
                index = i

        if index > -1:
            node = self.queue[index]
            del self.queue[index]
            return node
        else:
            return None

    def find(self, to_find):
        for node in self.queue:
            if to_find.board == node.board:
                return node
        return None

    def remove(self, to_find):
        for i in range(len(self)):
            if to_find.board == self.queue[i].board:
                del self.queue[i]
                return


def calculate_max():
    max_score = Board()
    max_score.spaces = [
        [Tile(2, True), Tile(3, True), Tile(6, True), Tile(12, True)],
        [Tile(96*2, True), Tile(96, True), Tile(48, True), Tile(24, True)],
        [Tile(96*4, True), Tile(96*8, True), Tile(96*16, True), Tile(96*32, True)],
        [Tile(96*512, True), Tile(96*256, True), Tile(96*128, True), Tile(96*64, True)]
    ]

    return max_score.calculate_score()


MAX_SCORE = calculate_max()


def a_star(cap=-1, print_nodes=False):
    open_queue = PriorityQueue()
    best_board = None
    best_score = 0
    num_checked = 0

    open_queue.enqueue(Node(Board()))
    while len(open_queue) > 0 and (cap < 0 or num_checked < cap):
        node = open_queue.dequeue()
        num_checked += 1

        if print_nodes:
            print(node.board)

        if node.board.calculate_score() >= MAX_SCORE:
            best_board = node.board
            break

        node.generate_next()
        if len(node.next) == 0 and node.board.calculate_score() > best_score:
            best_board = node.board
            best_score = node.board.calculate_score()
        else:
            for next_node in node.next:
                open_node = open_queue.find(next_node)

                if open_node is None:
                    open_queue.enqueue(next_node)

    return best_board.calculate_score(), best_board.max_value
