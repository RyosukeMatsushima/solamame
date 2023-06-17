import numpy as np

from modules.dynamic_programming.functions_base import FunctionsBase


class Functions(FunctionsBase):
    def __init__(
        self,
        state_space,
        control_inputs_set,
        time_step,
        goal_function,
        obstace_function,
        edge_cost,
    ):
        super().__init__(
            state_space,
            control_inputs_set,
            time_step,
            goal_function,
            obstace_function,
            edge_cost,
        )

        control_inputs_norm_set = [
            sum([control_input**2 for control_input in control_inputs]) ** 0.5
            for control_inputs in control_inputs_set
        ]
        self.control_inputs_cost_map_set = [
            np.ones(self.element_count) * (control_inputs_norm)
            for control_inputs_norm in control_inputs_norm_set
        ]

    def stage_cost_map(self, control_inputs):
        control_inputs_cost_map = self.control_inputs_cost_map_set[
            self.control_inputs_set.index(control_inputs)
        ]
        return self.obstacle_cost_map + self.edge_cost_map + control_inputs_cost_map + self.goal_cost_map * 0.01
