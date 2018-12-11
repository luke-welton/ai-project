# AI Project
COMP 5600: Artificial Intelligence Project on Threes!

### Quick start

> Clone/Download the solution then run `main.py`

```

# Download all files

# Run with Python 3.6 or higher
# Provide an algorithm selection. Use [0=montecarlo, 1=expectimax, 2=a_star, 3=greedy].

$ python main.py arg

```

# Table of Contents
* [Threes](#threes)
* [A*](#a-star)
* [Expectimax](#expectimax)
* [Monte Carlo](#monte-carlo)

## Threes

[threes](threes.py) contains our implementation of the game Threes! This file allows us to create a new game board, make 
moves on that board, place a new random tile, and calculate the board's current score. We use this implementation of the game 
in our algorithms to simulate playouts of the game in order to see which methods produce the best results.

___

## A Star

[a_star](a_star.py) contains our implementaion of A* search method. The A* search method allows us to essentially search 
for a path to the best possible score for Threes! with backtracking. This method was good for us to use as a baseline for 
possible high scores for Threes! and could be used to generate data for more advanced reinforcement learning if we were to 
expand further on this project. 

This file contains the method `a_star(cap=-1, print_nodes=False)`
The parameters are defined by the following:
- cap = The max score that A* will run to
- print_nodes = Whether or not each move board checked will be printed to the console

___

## Expectimax

[expectimax](expectimax.py) contains our implementaion of Expectimax. This file contains the method 
`expectimax(search_depth, print_boards=False)` 

The parameters are defined by the following:
- search_depth = The number of moves Expectimax will look ahead for each move it makes
- print_boards = Whether or not each move Expectimax makes is printed to the screen

The file also contains the method `run_expectimax(iterations, search_depth)` 

The parameters are defined by the following:
- iterations = how many runs of Expectimax(playing Threes! until it loses) should be simulated
- search_depth = The number of moves Expectimax will look ahead for each move it makes


___

## Monte Carlo
 
[montecarlo](montecarlo.py) contains our implementation of MonteCarlo. This file contains `run_monte_carlo(runs=[100, 50, 10, 5, 1], depths=[50, 100, 500, 1000, 5000], debug=False, print_results=True, save=False)`  

The parameters are defined by the following:  
- runs = The number of runs to make for each depth.
- depths = The amount of random playouts to make per run.
- debug = The option to print extraneous information.
- print_results = The option to print results as each run is being executed.
- save = The option to save final results to an output folder. If this is False they will open in windows instead.
