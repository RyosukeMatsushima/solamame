import numpy as np

from modules.dynamic_programming.dynamic_programming import DynamicProgramming
from modules.states_space.transition_matrix import *

from examples.common.dynamic_programming_common import *

from examples.dot_2d.base import Base

time_step = 0.05

end_threshold = 0.01
max_step = 100000
debug_frequency = 10

dumper = 0.99

base = Base()

calculate_dynamic_programming(
    base.statesSpace,
    base.get_stage_cost_map_set(time_step),
    base.get_transition_matrix_set(time_step),
    base.evaluate,
    base.inputs_set,
    base.terminal_cost_function,
    time_step,
    end_threshold,
    max_step,
    dumper,
    debug_frequency,
)
