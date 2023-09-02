import numpy as np
import copy
from tqdm import tqdm

# TODO: remove
import time


class FindCostToGo:
    def __init__(
        self,
        goal_probabilistic_space,
        transition_matrix_set,
        start_cost_map_set,
        cost_resolution,
        max_cost,
        init_cost,
        transition_matrix_set_normal,
    ):
        self.cost_to_go_space = copy.deepcopy(goal_probabilistic_space)
        self.inputs_space = copy.deepcopy(goal_probabilistic_space)

        self.goal_probabilistic_space = goal_probabilistic_space
        self.transition_matrix_set = transition_matrix_set
        self.start_cost_map_set = start_cost_map_set

        self.cost_resolution = cost_resolution
        self.max_cost = max_cost
        self.init_cost = init_cost

        self.transition_matrix_set_normal = transition_matrix_set_normal

    def calculate(self, is_reached_threshold):
        transition_matrix = np.sum(self.transition_matrix_set, axis=0) / len(
            self.transition_matrix_set
        )

        current_probablistic_space = self.goal_probabilistic_space.values

        # set -1 as invalid value
        # TODO: set init value as max cost
        cost_to_go = np.full_like(current_probablistic_space, self.max_cost)

        # calculate cost to go function
        for cost in tqdm(
            np.arange(self.init_cost, self.max_cost, self.cost_resolution)
        ):
            threshold = self.get_threshold(
                current_probablistic_space, is_reached_threshold
            )
            reachable_points = np.where(
                current_probablistic_space > threshold, cost, self.max_cost
            )
            cost_to_go = np.where(cost_to_go < cost, cost_to_go, reachable_points)

            current_probablistic_space = transition_matrix @ current_probablistic_space

        self.goal_probabilistic_space.values = cost_to_go

        # calculate input space
        next_value_function_set = (
            np.array(
                [
                    transition_matrix @ cost_to_go
                    for transition_matrix in self.transition_matrix_set_normal
                ]
            )
            + self.start_cost_map_set
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
