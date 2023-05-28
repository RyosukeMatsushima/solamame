import numpy as np

from tests.dynamic_programming.grid_2d_astar import astar


def cost_to_go(array, goal):
    cost_array = np.zeros(array.shape)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] <= 0:
                path, score = astar(array, goal, (i, j))
                cost_array[i][j] = score
            else:
                cost_array[i][j] = np.inf

    return cost_array


import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Define the grid as a 2D array
    grid = np.zeros((10, 10))  # initialize the grid with zeros

    # Add obstacle data to the grid
    grid[2][2] = 1  # set cell (2,2) as an obstacle
    grid[3][2] = 1
    grid[6][6] = 1
    grid[5][6] = 1
    grid[6][5] = 1
    grid[6][4] = 1
    grid[4][6] = 1
    grid[8][2] = 1

    # Define the start and goal points
    goal = (9, 9)

    cost_array = cost_to_go(grid, goal)

    print(cost_array)

    plt.figure()
    plt.imshow(cost_array)
    plt.show()
