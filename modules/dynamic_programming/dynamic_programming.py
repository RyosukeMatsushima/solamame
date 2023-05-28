#!/usr/bin/env python

import copy
import numpy as np

from modules.states_space.time_evolution_states_space import TimeEvolutionStatesSpace


class DynamicProgramming:
    def __init__(
        self,
        states_space,
        transition_matrix_set,
        stage_cost_map,
        terminal_cost_map,
        time_resolution,
        terminal_time,
        init_time,
        inputs_set,
    ):
        self.current_value_function = copy.deepcopy(states_space)
        self.transition_matrix_set = transition_matrix_set

        # stage_cost_map(inputs) return stage_cost for every state space elements.
        self.stage_cost_map = stage_cost_map
        self.terminal_cost_map = terminal_cost_map
        self.time_resolution = time_resolution
        self.terminal_time = terminal_time
        self.init_time = init_time
        self.inputs_set = inputs_set

        # TODO: create inpus_space
        self.inputs_space = TimeEvolutionStatesSpace(
            states_space, time_resolution, init_time, terminal_time
        )
        self.value_function = TimeEvolutionStatesSpace(
            states_space, time_resolution, init_time, terminal_time
        )

    def calculate(self, debug_func):
        time = self.terminal_time
        self.current_value_function = self.terminal_cost_map()

        self.value_function.set_value(time, self.current_value_function)

        while time > self.init_time:
            self.next_step(time)
            #debug_func(time)
            time -= self.time_resolution

        debug_func(time)

    def next_step(self, time):

        next_value_function_set = np.array( [self.stage_cost_map(inputs) + transition_matrix @ self.current_value_function for inputs, transition_matrix in zip(self.inputs_set, self.transition_matrix_set) ])
 
        #TODO: change stateSpace.values as ndarray.
        optimal_inputs_index = np.argmin(next_value_function_set, axis=0)

        self.current_value_function = np.choose(optimal_inputs_index, next_value_function_set)

        self.value_function.set_value(time, self.current_value_function)
        self.inputs_space.set_value(time, optimal_inputs_index)

