import numpy as np
from matplotlib import pyplot as plt
from math import log2

from montecarlo import run_monte_carlo
from expectimax import expectimax
from expectimax import run_expectimax
from A_Star import greedy

if __name__ == "__main__":

    # Monte Carlo
    run_monte_carlo(runs=[100,100,100,100], depths=[50,100,500,1000], save=True)

    # Expectimax
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
    plt.title(f'Expectimax Search Depth {search_depth} with Basic Heuristic')
    plt.show()

    # expectimax(3)

    # Greedy
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
