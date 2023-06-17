import unittest

import numpy as np

from modules.dynamic_programming.dynamic_programming_in_finite_time import DynamicProgramming
from modules.states_space.states_space import StatesSpace
from modules.states_space.transition_matrix import *

from tests.dynamic_programming.cost_to_go import cost_to_go
from tests.dynamic_programming.functions import Functions

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

        # create state space
        statesSpace = StatesSpace()

        statesSpace.add_axis("x", 0, 10, 1)
        statesSpace.add_axis("y", 0, 8, 1)

        statesSpace.create()

        def dynamic_func(state: "point as list", control_input):
            return np.array([control_input[0], control_input[1]])
            # return np.array(control_input)

        def is_goal(element_number):
            state = statesSpace.get_states_from(element_number)
            return state["x"] == self.goal[0] and state["y"] == self.goal[1]

        def is_obstace(element_number):
            state = statesSpace.get_states_from(element_number)
            return [state["x"], state["y"]] in obstacles

        functions = Functions(
            statesSpace, self.inputs_set, self.time_resolution, is_goal, is_obstace
        )

        # create transition matrix
        transition_matrix_set = get_transition_matrix(
            statesSpace, dynamic_func, self.inputs_set, self.time_resolution
        )

        self.dynamicProgramming = DynamicProgramming(
            statesSpace,
            transition_matrix_set,
            functions.stage_cost_map,
            functions.terminal_cost_map,
            self.time_resolution,
            8,
            0,
            self.inputs_set,
        )

    def test_with_2d_grid_astar(self):
        cost_array = cost_to_go(self.grid, self.goal)

        def debug_func(time):
            print("debug_func")
            # print(self.dynamicProgramming.value_function.get_state_space(time))
            sheet = self.dynamicProgramming.value_function.get_state_space(
                time
            ).get_2d_sheet("x", "y", {"x": 0, "y": 0})
            show_data(sheet)

            input_index = self.dynamicProgramming.inputs_space.get_state_space(
                time
            ).get_2d_sheet("x", "y", {"x": 0, "y": 0})
            print(input_index)
            show_data(input_index)

            input_vector_space = [
                [self.inputs_set[index] for index in l] for l in input_index
            ]
            print(input_vector_space)

            show_vector_field(np.array(input_vector_space))

        self.dynamicProgramming.calculate(debug_func)
