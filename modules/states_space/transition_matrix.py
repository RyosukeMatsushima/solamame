#!/usr/bin/env python

import numpy as np

from scipy.sparse import lil_matrix

from modules.states_space.states_space import StatesSpace

# TODO: remove
from modules.tools.fig_2d import *


def get_transition_matrix(state_space, dynamic_function, inputs_set, time_step):
    matrix_set = [
        lil_matrix((state_space.element_count, state_space.element_count))
        for _ in inputs_set
    ]

    for element_number in range(state_space.element_count):
        neighbors = state_space.get_neighbors_element_number(element_number)

        for inputs, matrix in zip(inputs_set, matrix_set):
            transition_vector = dynamic_function(element_number, inputs) * time_step

            probability_to_remain = 1.0
            for axis, transition_value in zip(state_space.axes, transition_vector):
                next_element = (
                    neighbors[axis.name][0]
                    # for dynamic programing we want max{ sum( V(x') P(x'|x, u) ) }.
                    if transition_value < 0
                    else neighbors[axis.name][1]
                )

                probability_to_go_next = abs(transition_value * axis.resolution)
                probability_to_remain -= probability_to_go_next

                if next_element is not None:
                    matrix[element_number, next_element] = probability_to_go_next

            if probability_to_remain < 0:
                raise ValueError("probability_to_remain < 0: time_step is too big")

            matrix[element_number, element_number] = probability_to_remain

    return matrix_set
