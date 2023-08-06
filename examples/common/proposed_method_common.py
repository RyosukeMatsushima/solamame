import numpy as np

from modules.proposed_method.find_cost_to_go import FindCostToGo
from modules.states_space.transition_matrix import *


def calculate_proposed_method(proballistic_space,
                              stage_cost_function,
                              dynamics,
                              evaluate,
                              inputs_set,
                              goal_state,
                              cost_resolution,
                              min_cost,
                              max_cost,
                              is_reached_threshold):

    def transition_function(element_number, inputs):
        states = list(proballistic_space.get_states_from(element_number).values())
        stage_cost = stage_cost_function(element_number, inputs)
        states_dt = dynamics(states, inputs) 

        if stage_cost <= 0:
            if not np.all(abs(states_dt) < 0.00000001):
                raise RuntimeError("invalid cost value. it's devided by zero")

            return np.zeros(len(states_dt))

        return states_dt / stage_cost

    # create transition matrix
    print("calculate transition_matrix_set")
    transition_matrix_set = get_transition_matrix(
        proballistic_space, transition_function, inputs_set, cost_resolution
    )

    goal_element_number = proballistic_space.get_element_number(goal_state)
    proballistic_space.values[goal_element_number] = 1
    
    findCostToGo = FindCostToGo(
        proballistic_space,
        transition_matrix_set,
        cost_resolution,
        max_cost,
        min_cost
    )

    print("start findCostToGo")
    findCostToGo.calculate(is_reached_threshold)
    
    evaluate(findCostToGo.inputs_space, findCostToGo.cost_to_go_space)

