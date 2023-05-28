import heapq


# Define the heuristic function
def heuristic(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Define the A* algorithm function
def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1], gscore.get(goal)

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [
                i[1] for i in oheap
            ]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False, False


import numpy as np

if __name__ == "__main__":
    # Define the grid as a 2D array
    grid = np.zeros((10, 10))  # initialize the grid with zeros

    # Add obstacle data to the grid
    grid[2][2] = 1  # set cell (2,2) as an obstacle
    grid[3][2] = 1  # set cell (3,2) as an obstacle
    grid[6][6] = 1  # set cell (6,6) as an obstacle
    grid[5][6] = 1  # set cell (6,6) as an obstacle
    grid[6][5] = 1  # set cell (6,6) as an obstacle

    # Define the start and goal points
    start = (0, 0)
    goal = (9, 9)

    # Find the shortest path using A*
    path, goal_score = astar(grid, start, goal)

    # Print the path
    print(path)
    print(goal_score)
