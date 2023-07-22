import numpy as np

from modules.proposed_method.find_cost_to_go import FindCostToGo
from modules.states_space.transition_matrix import *

from examples.single_pendulum.base import *

from modules.tools.fig_2d import *

time_resolution = 0.001
min_cost = 0
max_cost = 3

proballistic_space = statesSpace

def transition_function(element_number, inputs):
    states = list(proballistic_space.get_states_from(element_number).values())
    stage_cost = stage_cost_function(element_number, inputs)
    states_dt = dynamics(states, inputs) 

    if stage_cost <= 0:
        if not np.all(states_dt == 0.0):
            raise RuntimeError("invalid cost value. it's devided by zero")

        return np.zeros(len(states_dt))

    return states_dt / stage_cost

# create transition matrix
print("calculate transition_matrix_set")
transition_matrix_set = get_transition_matrix(
    proballistic_space, transition_function, inputs_set, time_resolution
)

goal_element_number = proballistic_space.get_element_number({"x": goal[0], "x_dot": goal[1]})
proballistic_space.values[goal_element_number] = 1

findCostToGo = FindCostToGo(
    proballistic_space,
    transition_matrix_set,
    time_resolution,
    max_cost,
    min_cost
)


print("start findCostToGo")
findCostToGo.calculate(10 ** (-2))

fig2D = Fig2D()
fig2D.add_img(np.array(findCostToGo.inputs_space.get_2d_sheet("x", "x_dot", {"x": 0, "x_dot": 0})).T)
fig2D.show()

fig2D = Fig2D()
fig2D.add_img(np.array(findCostToGo.cost_to_go_space.get_2d_sheet("x", "x_dot", {"x": 0, "x_dot": 0})).T)
fig2D.show()

evaluate(findCostToGo.inputs_space, findCostToGo.cost_to_go_space)
