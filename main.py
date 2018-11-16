from A_Star import a_star
import numpy
from matplotlib import pyplot as plt
from math import log2


if __name__ == "__main__":
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

    ind = numpy.arange(len(x_values))
    p = plt.bar(ind, counts)
    plt.title("A* Playing Threes! (1000 Cap)")
    plt.xlabel("Highest Tile Achieved")
    plt.ylabel("Count")
    plt.xticks(ind, x_values)
    plt.yticks(numpy.arange(0, max(counts), 10))
    plt.show()




