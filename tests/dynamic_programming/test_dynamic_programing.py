import unittest

import numpy as np

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.states_space import StatesSpace

from tests.dynamic_programming.cost_to_go import cost_to_go

# TODO: remove
from modules.tools.fig_2d import *


class TestDynamicProgramming(unittest.TestCase):
    def setUp(self):
        # Define the grid as a 2D array
        self.grid = np.zeros((10, 8))  # initialize the grid with zeros

        obstacles = [[5, 5], [4, 5], [5, 4], [3, 5]]
        # Add obstacle data to the grid
        #        grid[2][2] = 1  # set cell (2,2) as an obstacle
        #        grid[3][2] = 1
        #        grid[7][7] = 1

        self.inputs_set = [
            (0, 0),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        # Define the start and goal points
        self.goal = (2, 2)

        self.time_resolution = 0.1

        def dynamic_func(state: "point as list", control_input):
            return np.array([control_input[1], control_input[0]])
            # return np.array(control_input)

        def terminal_cost_func(state: "point as list"):
            # return ((state["x"] - goal[0]) ** 2 + (state["y"] - goal[1]) ** 2) ** 0.5
            if state["x"] == self.goal[0] and state["y"] == self.goal[1]:
                return 0
            else:
                return 100

        def stage_cost_func(state, control_input):
            if state:
                obstacle_cost = 100 if [state["x"], state["y"]] in obstacles else 0
            else:
                obstacle_cost = 0

            distance_cost = (
                (state["x"] - self.goal[0]) ** 2 + (state["y"] - self.goal[1]) ** 2
            ) ** 0.5 * 100

            return (
                (control_input[0] ** 2 + control_input[1] ** 2) ** 0.5
                + obstacle_cost
                + distance_cost
            )

        statesSpace = StatesSpace()

        statesSpace.add_axis("x", 0, 10, 1)
        statesSpace.add_axis("y", 0, 8, 1)

        statesSpace.create()

        self.dynamicProgramming = DynamicProgramming(
            statesSpace,
            dynamic_func,
            stage_cost_func,
            terminal_cost_func,
            self.time_resolution,
            8,
            0,
            self.inputs_set,
        )

    def test_with_2d_grid_astar(self):
        cost_array = cost_to_go(self.grid, self.goal)

        def debug_func(time):
            sheet = self.dynamicProgramming.current_value_function.get_2d_sheet(
                "x", "y", {"x": 0, "y": 0}
            )
            show_data(sheet)

            print(time)
            print(self.dynamicProgramming.inputs_space.get_state_space(time))
            sheet = self.dynamicProgramming.inputs_space.get_state_space(
                time
            ).get_2d_sheet("x", "y", {"x": 0, "y": 0})
            show_vector_field(np.array(sheet))

        self.dynamicProgramming.calculate(debug_func)

    def test_get_appropriate_input(self):
        print(self.dynamicProgramming.get_appropriate_input(np.array([0.0, 0.0]), None))
        print("aaaaaaaaaaaaaaaaaaaaaaa")
        print(
            self.dynamicProgramming.get_appropriate_input(np.array([12.0, 0.0]), None)
        )
