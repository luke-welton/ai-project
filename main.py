import numpy as np
from matplotlib import pyplot as plt
from math import log2
import sys

from montecarlo import run_monte_carlo
from expectimax import expectimax
from expectimax import run_expectimax
from A_Star import greedy
from A_Star import a_star

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide an algorithm selection. Use [0=montecarlo, 1=expectimax, 2=a_star, 3=greedy].")
        exit()
    selection = int(sys.argv[1])

    # Monte Carlo
    if selection == 0:
        print("Running Monte Carlo at depths [50,100,500,1000] for 100 runs each...")
        # Monte Carlo
        run_monte_carlo(runs=[100,100,100,100], depths=[50,100,500,1000], debug=False, print_results=False, save=True)
    
    # Expectimax
    elif selection == 1:
        print("Running Expectimax for 1000 runs...")
        search_depth = 3
        results = run_expectimax(1000, search_depth)
        high_tiles = results[0]
        high_scores = results[1]

        objects = ('12', '24', '48', '96', '192', '384', '786', '1536')
        y_pos = np.arange(len(objects))
        possible_values = [12, 24, 48, 96, 192, 384, 768, 1536]
        values = []
        for val in possible_values:
            values.append(high_tiles.count(val))

        plt.bar(y_pos, values, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.xlabel('Highest Tile Achieved')
        plt.ylabel('Count')
        plt.title('Expectimax Search Depth ' + search_depth + ' with Basic Heuristic')
        plt.show()
    
    # A Star
    elif selection == 2: 
        print("Running A* wih 2500 tile cap...")
        runs = 100
        max_tiles = []

        for _ in range(runs):
            score, max_tile = a_star(2500)
            max_tiles.append(max_tile)

        x_values = []
        counts = []
        for i in range(int(log2(max(max_tiles) / 12)) + 1):
            x_values.append(12 * 2 ** i)
            counts.append(0)

        for tile in max_tiles:
            counts[int(log2(tile / 12))] += 1

        ind = np.arange(len(x_values))
        p = plt.bar(ind, counts)
        plt.title("A* Playing Threes! (1000 Cap)")
        plt.xlabel("Highest Tile Achieved")
        plt.ylabel("Count")
        plt.xticks(ind, x_values)
        plt.yticks(np.arange(0, max(counts), 10))
        plt.show()

    # Greedy
    elif selection == 3:
        print("Running Greedy...")
        runs = 100
        max_tiles = []
        total_score = 0

        for _ in range(runs):
            score, max_tile = greedy()
            total_score += score
            max_tiles.append(max_tile)

        x_values = []
        counts = []
        for i in range(max(int(log2(max(max_tiles) / 12)) + 1, 8)):
            x_values.append(12 * 2 ** i)
            counts.append(0)

        for tile in max_tiles:
            counts[max(int(log2(tile / 12)), 0)] += 1

        ind = np.arange(len(x_values))

        plt.bar(ind, counts)
        plt.title("Greedy Playing Threes!")
        plt.xlabel("Highest Tile Achieved")
        plt.ylabel("Count")
        plt.xticks(ind, x_values)
        plt.show()

        print("Average Score: {}".format(total_score / runs))
    else:
        print("Invalid algorithm selection. Use [0=montecarlo, 1=expectimax, 2=a_star, 3=greedy].")
