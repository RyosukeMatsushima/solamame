import numpy as np
import time

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.transition_matrix import *

from examples.single_pendulum.base import *


def calculate_dynamic_programming(
    statesSpace,
    stage_cost_map_set,
    transition_matrix_set,
    evaluate,
    inputs_set,
    terminal_cost_function,
    time_step,
    end_threshold,
    max_step,
    debug_frequency,
):
    def terminal_cost_map():
        return np.array(
            [
                terminal_cost_function(element_number)
                for element_number in range(statesSpace.element_count)
            ]
        )

    start_time = time.time()

    dynamicProgramming = DynamicProgramming(
        statesSpace,
        transition_matrix_set,
        stage_cost_map_set,
        terminal_cost_map,
        inputs_set,
        end_threshold,
        max_step,
        debug_frequency,
    )

    def debug_func(step, evaluation_value):
        print("debug_func")
        print("step: {}, evaluation_value: {}".format(step, evaluation_value))

    dynamicProgramming.calculate(debug_func)

    elapsed_time = time.time() - start_time
    print("elapsed_time: {} [sec]".format(elapsed_time))

    evaluate(dynamicProgramming.inputs_space, dynamicProgramming.current_value_function)

