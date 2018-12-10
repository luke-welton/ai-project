from expectimax import expectimax
from expectimax import run_expectimax

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
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

