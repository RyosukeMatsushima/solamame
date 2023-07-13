import numpy as np

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.transition_matrix import *

from examples.dot_2d.base import *

time_step = 0.1

def stage_cost_map(inputs):
    return np.array([stage_cost_function(element_number, inputs) for element_number in range(statesSpace.element_count)]) * time_step

def terminal_cost_map():
    return np.array([terminal_cost_function(element_number) for element_number in range(statesSpace.element_count)])

def transition_function(element_number, inputs):
    states = list(statesSpace.get_states_from(element_number).values())
    return dynamics(states, inputs)


# create transition matrix
transition_matrix_set = get_transition_matrix(
    statesSpace, transition_function, inputs_set, time_step
)

dynamicProgramming = DynamicProgramming(
    statesSpace,
    transition_matrix_set,
    stage_cost_map,
    terminal_cost_map,
    inputs_set,
    0.00001,
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

evaluate(dynamicProgramming.inputs_space, dynamicProgramming.current_value_function)
