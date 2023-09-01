import numpy as np

from modules.proposed_method.find_cost_to_go import FindCostToGo
from modules.states_space.transition_matrix import *

from examples.common.proposed_method_common import *

from examples.dot_2d.base import Base

cost_resolution = 0.01
min_cost = 0
max_cost = 300
is_reached_threshold = 10 ** (-8)

base = Base()

calculate_proposed_method(
    base.statesSpace,
    base.stage_cost_function,
    base.dynamics,
    base.evaluate,
    base.inputs_set,
    base.goal_state,
    cost_resolution,
    min_cost,
    max_cost,
    is_reached_threshold,
)
