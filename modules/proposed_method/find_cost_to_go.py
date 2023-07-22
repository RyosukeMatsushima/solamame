import numpy as np
import copy
from tqdm import tqdm

from modules.states_space.time_evolution_states_space import TimeEvolutionStatesSpace

# TODO: remove
import time

class FindCostToGo:
    def __init__(
        self,
        goal_probabilistic_space,
        transition_matrix_set,
        cost_resolution,
        max_cost,
        init_cost,
        ):

        self.cost_to_go_space = copy.deepcopy(goal_probabilistic_space)
        self.inputs_space = copy.deepcopy(goal_probabilistic_space)

        self.goal_probabilistic_space = goal_probabilistic_space
        self.transition_matrix_set = transition_matrix_set

        self.cost_resolution = cost_resolution
        self.max_cost = max_cost
        self.init_cost = init_cost


    def calculate(self, is_reached_threshold):

        # TODO: create inpus_space
        #TODO: remove
        probabilistic_function = TimeEvolutionStatesSpace(
            self.goal_probabilistic_space, 1/self.cost_resolution, self.init_cost, self.max_cost
        )

        transition_matrix = np.sum(self.transition_matrix_set, axis=0) / len(self.transition_matrix_set)

        current_probablistic_space = self.goal_probabilistic_space.values

        # set -1 as invalid value
        #TODO: set init value as max cost
        cost_to_go = np.full_like(current_probablistic_space, -1)

        #TODO: remove
        probabilistic_function.set_value(self.init_cost, current_probablistic_space)

        # calculate cost to go function
        for i in tqdm(range(probabilistic_function.time_axis.length)):
            cost = probabilistic_function.time_axis.get_value(i)
            current_probablistic_space = transition_matrix @ current_probablistic_space

            #TODO: remove
            probabilistic_function.set_value(cost, current_probablistic_space)

            threshold = self.get_threshold(current_probablistic_space, is_reached_threshold)
            reachable_points = np.where(current_probablistic_space > threshold, cost, -1)
            cost_to_go = np.where(cost_to_go > 0, cost_to_go, reachable_points)

        self.goal_probabilistic_space.values = cost_to_go

        # calculate input space
        next_value_function_set = np.array(
            [
                transition_matrix @ cost_to_go
                for transition_matrix in self.transition_matrix_set
            ]
        )

        # TODO: change stateSpace.values as ndarray.
        optimal_inputs_index = np.argmin(next_value_function_set, axis=0)

        self.cost_to_go_space.values = cost_to_go
        self.inputs_space.values = optimal_inputs_index

    def get_threshold(self, values, a):
        values = np.sort(values)
        cumsum = np.cumsum(values)
        total_sum = cumsum[-1]

        return values[np.argmax(cumsum > total_sum * a) - 1]

