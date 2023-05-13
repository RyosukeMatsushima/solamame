#!/usr/bin/env python

import copy

from modules.states_space.time_evolution_states_space import TimeEvolutionStatesSpace


class DynamicProgramming:
    def __init__(
        self,
        states_space,
        dynamics_func,
        stage_cost_func,
        terminal_cost_func,
        time_resolution,
        terminal_time,
        init_time,
        inputs_set,
    ):
        self.current_value_function = copy.deepcopy(states_space)
        self.dynamics_func = dynamics_func
        self.stage_cost_func = stage_cost_func
        self.terminal_cost_func = terminal_cost_func
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
        elements_count = self.current_value_function.element_count
        time = self.terminal_time

        for element_number in range(elements_count):
            states = self.current_value_function.get_states_from(element_number)
            terminal_value = self.terminal_cost_func(states)
            self.current_value_function.set_value(element_number, terminal_value)
            print(element_number)
            print(states)
            print(terminal_value)

        self.value_function.set_value(time, self.current_value_function)

        while time > self.init_time:
            self.next_step(time)
            # debug_func(time)
            time -= self.time_resolution

        debug_func(time)

    def next_step(self, time):
        elements_count = self.current_value_function.element_count

        current_input_space = copy.deepcopy(self.current_value_function)
        latest_value_function = copy.deepcopy(self.current_value_function)

        for element_number in range(elements_count):
            states = self.current_value_function.get_states_from(element_number)
            gradient_vector = latest_value_function.get_gradient(element_number)
            appropriate_input, hamiltonian = self.get_appropriate_input(
                gradient_vector, states
            )

            current_input_space.set_value(element_number, appropriate_input)

            self.current_value_function.add_value(
                element_number, -hamiltonian * self.time_resolution
            )

        self.value_function.set_value(time, self.current_value_function)
        self.inputs_space.set_value(time, current_input_space)

    def get_appropriate_input(self, gradient_vector, states):
        if abs(gradient_vector[0]) > 1 or abs(gradient_vector[1]) > 1:
            print("")
            print("")
            print("get_appropriate_input")

        minimum_hamiltonian = None
        appropriate_input = None

        for control_input in self.inputs_set:
            hamiltonian = self.stage_cost_func(
                states, control_input
            ) - gradient_vector @ self.dynamics_func(states, control_input)

            if abs(gradient_vector[0]) > 1 or abs(gradient_vector[1]) > 1:
                # if True:
                print("")
                print("gradient_vector")
                print(gradient_vector)
                print(control_input)
                print(gradient_vector @ self.dynamics_func(states, control_input))
                print(self.stage_cost_func(states, control_input))
                print(hamiltonian)

                print("appropriate_input")
                print(appropriate_input)
                print("minimum_hamiltonian")
                print(minimum_hamiltonian)

            if minimum_hamiltonian is not None:
                if minimum_hamiltonian < hamiltonian:
                    if abs(gradient_vector[0]) > 1 or abs(gradient_vector[1]) > 1:
                        print("continue")
                    continue

            minimum_hamiltonian = hamiltonian
            appropriate_input = control_input

        return appropriate_input, minimum_hamiltonian
