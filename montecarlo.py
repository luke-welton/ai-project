import random, time
import numpy as np
from threes import Board, Directions, Tile, InvalidMove
from matplotlib import pyplot as plt

class MonteCarlo:

    def __init__(self, depth=50, run=0, debug=False, print_results=True, plot=False):
        self.board = Board()
        self.run = run
        self.depth = depth
        self.score = 0
        self.highest_tile = 0
        self.moves = 0
        self.score_progress = []
        self.playout_score_progress = []
        self.debug = debug
        self.print_results = print_results
        self.plot = plot

    def reset(self):
        self.board = Board()
        self.score = 0
        self.moves = 0
        self.highest_tile = 0
        self.score_progress = []
        self.playout_score_progress = []

    # Begin playing the board.
    def start(self):
        self.reset()
        self.run += 1
        while self.board.has_moves():
            direction = self.get_next_direction()
            self.board.move(direction)
            self.score = self.board.calculate_score()
            self.score_progress.append(self.score)
            self.moves += 1
            if self.debug:
                print("Choosing " + str(direction) + ". New Score: " + str(self.score))
        self.highest_tile = self.board.max_value
        if self.print_results:
            print("[" + str(self.depth) + "]#" + str(self.run) + " | Score: " + str(self.score) + " | Highest tile: " + str(self.highest_tile) + " | Moves: " + str(self.moves))
        if self.debug:
            print(self.board)
        if self.plot:
            self.graph_results()

    # Calculate the next move from the current state of the board.
    def get_next_direction(self):
        best_move = None
        highest_score = 0
        for direction in Directions:
            avg_score = self.get_direction_score(direction)
            if avg_score > highest_score:
                highest_score = avg_score
                best_move = direction
        self.playout_score_progress.append(highest_score)
        if self.debug:
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
            playout_board.move(d)
        score = playout_board.calculate_score()
        return score

    def graph_results(self):
        plt.plot(self.score_progress)
        plt.plot(self.playout_score_progress)
        plt.title('Predicted Score vs Actual for Depth ' + str(self.depth))
        plt.ylabel('Score')
        plt.xlabel('Moves')
        #plt.show()
        plt.savefig(str(self.depth) + '_converge.png')
        return True

# Collect data on the MonteCarlo implementation.
def run_monte_carlo(runs=[100, 50, 10, 5, 1], depths=[50, 100, 500, 1000, 5000], debug=False, print_results=True, save=False):
    scores = {}
    moves = {}
    tiles = {}
    avg_scores = [0] * len(depths)
    min_tiles = [0] * len(depths)
    max_tiles = [0] * len(depths)

    # Set empty arrays in dictionaries
    for depth in depths:
        scores[depth] = []
        moves[depth] = []
        tiles[depth] = []

    # Run simulations
    mc = MonteCarlo(debug=debug, print_results=print_results)
    for index, depth in enumerate(depths):
        mc.depth = depth
        mc.run = 0
        avg_score = 0
        min_tile = 100000
        max_tile = 0
        start = int(round(time.time() * 1000))
        for i in range(runs[index]):
            mc.start()
            scores[depth].append(mc.score)
            avg_score += mc.score
            moves[depth].append(mc.moves)
            tiles[depth].append(mc.highest_tile)
            if mc.highest_tile < min_tile:
                min_tile = mc.highest_tile
            if mc.highest_tile > max_tile:
                max_tile = mc.highest_tile
            mc.graph_results()
        end = int(round(time.time() * 1000))
        elapsed = (end - start) / 1000
        avg_score /= runs[index]
        avg_scores[index] = avg_score
        min_tiles[index] = min_tile
        max_tiles[index] = max_tile
        if print_results:
            print ('[' + str(mc.depth) + '] Time taken: ' + str(elapsed) + ' seconds')
            print ('[' + str(mc.depth) + '] Average score: ' + str(avg_scores[index]) + ' | Min tile: ' + str(min_tiles[index]) + ' | Max tile: ' +str(max_tiles[index]))
        graph_results(mc.depth + 1, scores[depth], 'Playout Score for Depth ' + str(mc.depth), 'Score', save)
        graph_results(mc.depth + 2, moves[depth], '# of Moves for Depth ' + str(mc.depth), 'Move', save)
        graph_results(mc.depth + 3, tiles[depth], 'Highest Tile for Depth ' + str(mc.depth), 'Highest Tile', save)

    box_results(mc.depth + 4, avg_scores, depths, 'Average Scores for Depths', 'Average Score')
    box_results(mc.depth + 5, max_tiles, depths, 'Highest Tiles for Depths', 'Tile')

def graph_results(run, data, title, ytitle, save=False):
    plt.figure(run)
    plt.plot(data)
    plt.title(title)
    plt.ylabel(ytitle)
    plt.xlabel('Trial #')
    if save:
        plt.savefig(title.lower().replace(' ', '_') + ".png")
    else:
        plt.plot()

def box_results(run, data, depths, title, ylabel):
    plt.figure(run)
    y_pos = np.arange(len(depths))
    plt.bar(y_pos, data, align='center')
    plt.xticks(y_pos, depths)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig(title.lower().replace(' ', '_') + ".png")

# Here we go.     
run_monte_carlo(runs=[1], depths=[1000], save=True, debug=True)