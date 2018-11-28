import random
from threes import Board, Directions, Tile, InvalidMove
from matplotlib import pyplot as plt

class MonteCarlo:

    def __init__(self, depth):
        self.board = Board()
        self.depth = depth
        self.score_progress = []
        self.playout_score_progress = []

    # Begin playing the board.
    def start(self):
        score = 0
        while self.board.has_moves():
            direction = self.get_next_direction()
            self.board.move(direction)
            score = self.board.calculate_score()
            print("Choosing " + str(direction) + ". New Score: " + str(score))
        print("Ended with score: " + str(score) + " Highest tile: " + str(self.board.max_value))
        print(self.board)

    # Calculate the next move from the current state of the board.
    def get_next_direction(self):
        best_move = None
        highest_score = 0
        for direction in Directions:
            avg_score = self.get_direction_score(direction)
            if avg_score > highest_score:
                highest_score = avg_score
                best_move = direction
        print("Best move is " + str(best_move) + " with highest score: " + str(highest_score))
        return best_move

    # Playout the game {depth} number of times
    #   in order to get the average score for the given direction.
    # Update total score after a full termination of a playout.
    def get_direction_score(self, direction):
        total_score = 0
        for i in range(self.depth):
            playout_score = self.random_playout(direction)
            total_score += playout_score
        return total_score / self.depth

    # Move the board in the inital direction,
    #   and then continue random playout until losing.
    def random_playout(self, direction):
        directions = list(Directions)
        playout_board = Board(self.board)
        score = 0
        moved = playout_board.move(direction)
        if moved == False:
            return 0
        while playout_board.has_moves():
            d = random.choice(directions)
            if d == None:
                continue
            playout_board.move(d)
        score = playout_board.calculate_score()
        return score

    def graph_results(self):
        return True


# start
mc = MonteCarlo(500)
mc.start()