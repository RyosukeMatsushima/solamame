import numpy as np

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.states_space import StatesSpace
from modules.states_space.transition_matrix import *

from submodules.physics_simulator.dot_2d.dot_2d import Dot2D

from tests.dynamic_programming.cost_to_go import cost_to_go
from tests.dynamic_programming.functions import Functions

from examples.dot_2d.simulate import simulate

# TODO: remove
from modules.tools.fig_2d import *


obstacles = [[5, 5], [4, 5], [5, 4], [3, 5]]
# Add obstacle data to the grid
#        grid[2][2] = 1  # set cell (2,2) as an obstacle
#        grid[3][2] = 1
#        grid[7][7] = 1

inputs_set = [
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
goal = (2, 2)

time_resolution = 0.1
start_time = 0
end_time = 12

# create state space
statesSpace = StatesSpace()

statesSpace.add_axis("x", 0, 10, 1)
statesSpace.add_axis("y", 0, 8, 1)

statesSpace.create()


def is_goal(element_number):
    state = statesSpace.get_states_from(element_number)
    return state["x"] == goal[0] and state["y"] == goal[1]

def is_obstace(element_number):
    state = statesSpace.get_states_from(element_number)
    return [state["x"], state["y"]] in obstacles


functions = Functions(statesSpace, inputs_set, time_resolution, is_goal, is_obstace)


# create transition matrix
transition_matrix_set = get_transition_matrix(
    statesSpace, Dot2D([0.0, 0.0]).dynamics, inputs_set, time_resolution
)

dynamicProgramming = DynamicProgramming(
    statesSpace,
    transition_matrix_set,
    functions.stage_cost_map,
    functions.terminal_cost_map,
    time_resolution,
    end_time,
    start_time,
    inputs_set,
)


def debug_func(time):
    print("debug_func")
    #print(dynamicProgramming.value_function.get_state_space(time))
    sheet = dynamicProgramming.value_function.get_state_space(time).get_2d_sheet(
        "x", "y", {"x": 0, "y": 0}
    )
    show_data(sheet)


    input_index = dynamicProgramming.inputs_space.get_state_space(time).get_2d_sheet(
        "x", "y", {"x": 0, "y": 0}
    )
    print(input_index)
    show_data(input_index)

    input_vector_space = [ [ inputs_set[index] for index in l ] for l in input_index ]
    print(input_vector_space)

    show_vector_field(np.array(input_vector_space))


dynamicProgramming.calculate(debug_func)

init_state = {"x": 8, "y": 7}
simulate(dynamicProgramming.inputs_space, inputs_set, start_time, end_time, init_state)

