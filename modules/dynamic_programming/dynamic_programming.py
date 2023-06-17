#!/usr/bin/env python

import copy
import numpy as np


class DynamicProgramming:
    def __init__(
        self,
        states_space,
        transition_matrix_set,
        stage_cost_map,
        terminal_cost_map,
        inputs_set,
        end_threshold,
        max_step,
        debug_frequency
    ):
        self.current_value_function = copy.deepcopy(states_space)
        self.inputs_space = copy.deepcopy(states_space)
        self.transition_matrix_set = transition_matrix_set

        # stage_cost_map(inputs) return stage_cost for every state space elements.
        self.stage_cost_map = stage_cost_map
        self.terminal_cost_map = terminal_cost_map
        self.inputs_set = inputs_set
        self.end_threshold = end_threshold
        self.max_step = max_step
        self.debug_frequency = debug_frequency

    def calculate(self, debug_func):
        self.current_value_function.values = self.terminal_cost_map()

        step = 0
        while step < self.max_step:
            if self.next_step():
                debug_func()
                return True

            if step % self.debug_frequency == 0:
                debug_func()

            step += 1

        debug_func()
        raise ValueError("over max_step")

    def next_step(self):
        next_value_function_set = np.array(
            [
                self.stage_cost_map(inputs)
                + transition_matrix @ self.current_value_function.values
                for inputs, transition_matrix in zip(
                    self.inputs_set, self.transition_matrix_set
                )
            ]
        )

        # TODO: change stateSpace.values as ndarray.
        optimal_inputs_index = np.argmin(next_value_function_set, axis=0)

        new_value_function = np.choose(
            optimal_inputs_index, next_value_function_set
        )

        if np.all(abs(new_value_function - self.current_value_function.values) < self.end_threshold):
            return True

        self.current_value_function.values = new_value_function
        self.inputs_space.values = optimal_inputs_index

        return False

