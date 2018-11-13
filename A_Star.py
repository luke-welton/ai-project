from threes import Board, Directions, Tile, InvalidMove


class Node:
    def __init__(self, board, prev=None):
        self.board = board
        self.next = []
        self.prev = prev

        self.move_count = 1
        if prev is not None:
            self.move_count += prev.move_count

        self.distance = MAX_SCORE - board.calculate_score() + self.move_count

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
            if index < 0 or self.queue[i].distance < self.queue[index].distance:
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


def a_star(print_nodes=False):
    open_queue = PriorityQueue()
    closed_queue = PriorityQueue()
    best_score = 0

    open_queue.enqueue(Node(Board()))
    while len(open_queue) > 0:
        node = open_queue.dequeue()
        closed_queue.enqueue(node)

        if print_nodes:
            print(node.board)
            print(best_score)

        if node.board.score >= MAX_SCORE:
            best_score = node.board.score
            break

        node.generate_next()
        if len(node.next) == 0 and node.board.score > best_score:
            best_score = node.board.score
        else:
            for next_node in node.next:
                open_node = open_queue.find(next_node)
                closed_node = closed_queue.find(next_node)

                if open_node is None:
                    open_queue.enqueue(next_node)

                    if closed_node is not None:
                        closed_queue.remove(closed_node)
                elif next_node.distance < open_node.distance:
                    open_node.update_node(next_node)

    print("Best Score for A*:\t{}".format(best_score))
