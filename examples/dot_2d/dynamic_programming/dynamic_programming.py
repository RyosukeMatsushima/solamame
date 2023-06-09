import numpy as np

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.states_space import StatesSpace
from modules.states_space.transition_matrix import *

from submodules.physics_simulator.dot_2d.dot_2d import Dot2D

from examples.dot_2d.dynamic_programming.functions import Functions

from examples.dot_2d.dynamic_programming.simulate import simulate

# TODO: remove
from modules.tools.fig_2d import *


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
goal = (4, 2)

time_resolution = 0.1
start_time = 0
end_time = 18

# create state space
statesSpace = StatesSpace()

statesSpace.add_axis("x", 0, 10, 3)
statesSpace.add_axis("y", 0, 8, 3)

statesSpace.create()


def goal_function(element_number):
    state = statesSpace.get_states_from(element_number)
    is_goal = state["x"] == goal[0] and state["y"] == goal[1]
    return 0.0 if is_goal else 100.0


def is_obstacle(element_number):
    state = statesSpace.get_states_from(element_number)

    if 1 < state["x"] < 3 and 5 < state["y"] < 6:
        return True
    if 4 < state["x"] < 7 and 5 < state["y"] < 6:
        return True
    if 2 < state["x"] < 5 and 3 < state["y"] < 4:
        return True

    return False


def obstace_function(element_number):
    return 100000.0 if is_obstacle(element_number) else 0.0

def dynamics_function(element_number, inputs):
    states = list(statesSpace.get_states_from(element_number).values())
    return Dot2D([0.0, 0.0]).dynamics(states, inputs)


functions = Functions(
    statesSpace, inputs_set, time_resolution, goal_function, obstace_function, 100
)


# create transition matrix
transition_matrix_set = get_transition_matrix(
    statesSpace, dynamics_function, inputs_set, time_resolution
)

dynamicProgramming = DynamicProgramming(
    statesSpace,
    transition_matrix_set,
    functions.stage_cost_map,
    functions.terminal_cost_map,
    inputs_set,
    0.00000000000001,
    100000,
    600
)


def debug_func():
    print("debug_func")
    sheet = dynamicProgramming.current_value_function.get_2d_sheet(
        "x", "y", {"x": 0, "y": 0}
    )
    sheet = np.array(sheet)
    sheet = np.where(sheet > 60, 60, sheet)
    show_data(sheet)

    input_index = dynamicProgramming.inputs_space.get_2d_sheet(
        "x", "y", {"x": 0, "y": 0}
    )
    print(input_index)
    show_data(input_index)

    input_vector_space = [[inputs_set[index] for index in l] for l in input_index]
    print(input_vector_space)

    show_vector_field(np.array(input_vector_space))


dynamicProgramming.calculate(debug_func)

init_state = {"x": 3, "y": 7}

result = simulate(
    dynamicProgramming.inputs_space, inputs_set, start_time, end_time, init_state
)

fig2D = Fig2D()

state_space = dynamicProgramming.current_value_function

state_space.values = functions.obstacle_cost_map

fig2D.add_img(np.array(state_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})).T)
fig2D.add_line(
    "path",
    [
        result["X"].to_numpy() * state_space.axis_named("x").resolution,
        result["Y"].to_numpy() * state_space.axis_named("y").resolution,
    ],
)


input_index = dynamicProgramming.inputs_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})
input_vector_space = np.array([[inputs_set[index] for index in l] for l in input_index])
fig2D.add_vector_field("inputs_space", input_vector_space)

fig2D.show()

print(result["X"].to_numpy())
