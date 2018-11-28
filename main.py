from A_Star import greedy
import numpy as np
from matplotlib import pyplot as plt
from math import log2


if __name__ == "__main__":
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
