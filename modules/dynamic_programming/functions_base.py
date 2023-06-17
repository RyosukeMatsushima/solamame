import numpy as np


class FunctionsBase:
    def __init__(
        self,
        state_space,
        control_inputs_set,
        time_step,
        goal_function,
        obstace_function,
        edge_cost,
    ):
        self.element_count = state_space.element_count
        self.control_inputs_set = control_inputs_set
        self.time_step = time_step
        self.goal_function = goal_function

        self.obstacle_cost_map = np.array(
            [
                obstace_function(element_number)
                for element_number in range(self.element_count)
            ]
        )

        self.edge_cost_map = np.zeros(self.element_count)
        for i in range(self.element_count):
            neigbors = state_space.get_neighbors_element_number(i)
            is_edge = True in [None in i for i in neigbors.values()]

            if is_edge:
                self.edge_cost_map[i] = edge_cost

        self.goal_cost_map = self.terminal_cost_map()

    def terminal_cost_map(self):
        return np.array(
            [
                self.goal_function(element_number)
                for element_number in range(self.element_count)
            ]
        )

    def stage_cost_map(self, control_inputs):
        return
