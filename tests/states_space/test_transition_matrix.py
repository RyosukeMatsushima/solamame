import unittest

import numpy as np

from modules.states_space.states_space import StatesSpace
from modules.states_space.transition_matrix import *


# TODO: remove
from modules.tools.fig_2d import *


class TestTransitionMatrix(unittest.TestCase):
    def test_transition_matrix(self):
        inputs_set = [
            (0, 0),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

        time_resolution = 0.1

        def dynamic_func(state: "point as list", control_input):
            return np.array([control_input[0], control_input[1]])

        # create state space
        statesSpace = StatesSpace()

        statesSpace.add_axis("x", -3, 1, 1)
        statesSpace.add_axis("y", -1, 9, 0.5)

        statesSpace.create()

        # create transition matrix
        transition_matrix_set = get_transition_matrix(
            statesSpace, dynamic_func, inputs_set, time_resolution
        )
        # [show_data(transition_matrix.toarray()) for transition_matrix in transition_matrix_set]
        # [show_data((transition_matrix - transition_matrix_set[0]).toarray()) for transition_matrix in transition_matrix_set]

        self.assertEqual(statesSpace.element_count, 5 * 7)

        for inputs, transition_matrix in zip(inputs_set, transition_matrix_set):
            if inputs == (0, 0):
                expect = np.zeros(
                    (statesSpace.element_count, statesSpace.element_count)
                )
                for element_number in range(statesSpace.element_count):
                    expect[element_number, element_number] = 1.0

                self.assertTrue(np.all(expect == transition_matrix.toarray()))

                # multiple result test.
                test_x = np.array([i for i in range(statesSpace.element_count)])
                result = transition_matrix @ test_x

                expect = np.zeros(statesSpace.element_count)
                for element_number in range(statesSpace.element_count):
                    expect[element_number] = element_number

                self.assertTrue(np.all(expect == result))

            if inputs == (-1, 0):
                delta = abs(
                    time_resolution * inputs[0] * statesSpace.axes[0].resolution
                )
                expect = np.zeros(
                    (statesSpace.element_count, statesSpace.element_count)
                )
                for element_number in range(statesSpace.element_count):
                    expect[element_number, element_number] = 1.0 - delta

                    lower_element_number = element_number - 1
                    if element_number % statesSpace.axes[0].length >= 1:
                        expect[element_number, lower_element_number] = delta

                self.assertTrue(np.all(expect == transition_matrix.toarray()))

                # multiple result test.
                test_x = np.array([i for i in range(statesSpace.element_count)])
                result = transition_matrix @ test_x

                expect = np.zeros(statesSpace.element_count)
                for element_number in range(statesSpace.element_count):
                    expect[element_number] = element_number * (1.0 - delta)
                    lower_element_number = element_number - 1
                    if element_number % statesSpace.axes[0].length >= 1:
                        expect[element_number] += lower_element_number * delta

                self.assertTrue(np.all(expect == result))

            if inputs == (0, 1):
                delta = time_resolution * inputs[1] * statesSpace.axes[1].resolution
                expect = np.zeros(
                    (statesSpace.element_count, statesSpace.element_count)
                )
                for element_number in range(statesSpace.element_count):
                    expect[element_number, element_number] = 1.0 - delta

                    upper_element_number = element_number + statesSpace.axes[0].length
                    if element_number % statesSpace.element_count < (
                        statesSpace.element_count - statesSpace.axes[0].length
                    ):
                        expect[element_number, upper_element_number] = delta

                # show_data(expect)
                # show_data(transition_matrix.toarray())
                # show_data(transition_matrix.toarray() - expect)

                self.assertTrue(np.all(expect == transition_matrix.toarray()))

                # multiple result test.
                test_x = np.array([i for i in range(statesSpace.element_count)])
                result = transition_matrix @ test_x

                expect = np.zeros(statesSpace.element_count)
                for element_number in range(statesSpace.element_count):
                    expect[element_number] = element_number * (1.0 - delta)
                    upper_element_number = element_number + statesSpace.axes[0].length
                    if element_number % statesSpace.element_count < (
                        statesSpace.element_count - statesSpace.axes[0].length
                    ):
                        expect[element_number] += upper_element_number * delta

                self.assertTrue(np.all(expect == result))
