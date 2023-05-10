import unittest
import numpy as np

from modules.states_space.states_space import StatesSpace


class StatesSpaceTest(unittest.TestCase):
    def setUp(self):
        self.statesSpace = StatesSpace()

    def test_get_states(self):
        reference_axes = [
            {"name": "a0", "min_value": -1.0, "max_value": 2.0, "resolution": 4},
            {"name": "a1", "min_value": -1.5, "max_value": 2.3, "resolution": 5},
            {"name": "a2", "min_value": 0.7, "max_value": 1.3, "resolution": 4},
        ]

        for axis in reference_axes:
            self.statesSpace.add_axis(
                axis["name"], axis["min_value"], axis["max_value"], axis["resolution"]
            )

        self.statesSpace.create()

        for element_number_input in range(self.statesSpace.element_count):
            states = self.statesSpace.get_states_from(element_number_input)

            element_number_output = self.statesSpace.get_element_number(states)

            self.assertEqual(element_number_input, element_number_output)

    def test_get_gradient(self):
        reference_axes = [
            {"name": "a0", "min_value": -1.0, "max_value": 1.0, "resolution": 1},
            {"name": "a1", "min_value": -1.0, "max_value": 1.0, "resolution": 1},
            {"name": "a2", "min_value": -1.0, "max_value": 1.0, "resolution": 1},
        ]

        for axis in reference_axes:
            self.statesSpace.add_axis(
                axis["name"], axis["min_value"], axis["max_value"], axis["resolution"]
            )

        self.statesSpace.create()

        for element_number in range(self.statesSpace.element_count):
            self.statesSpace.set_value(element_number, element_number**2)

        gradient_vector = self.statesSpace.get_gradient(0)
        expect_gradient_vector = np.array([1.0, 9.0, 81.0])
        self.assertEqual(gradient_vector.tolist(), expect_gradient_vector.tolist())

        gradient_vector = self.statesSpace.get_gradient(13)
        expect_gradient_vector = np.array(
            [
                (14.0**2 - 12.0**2) / 2,
                (16.0**2 - 10.0**2) / 2,
                (22.0**2 - 4.0**2) / 2,
            ]
        )
        self.assertEqual(gradient_vector.tolist(), expect_gradient_vector.tolist())

    def test_get_gradient_with_same_value(self):
        reference_axes = [
            {"name": "a0", "min_value": -1.0, "max_value": 1.0, "resolution": 1},
            {"name": "a1", "min_value": -1.0, "max_value": 1.0, "resolution": 1},
        ]

        for axis in reference_axes:
            self.statesSpace.add_axis(
                axis["name"], axis["min_value"], axis["max_value"], axis["resolution"]
            )

        self.statesSpace.create()

        for element_number in range(self.statesSpace.element_count):
            self.statesSpace.set_value(element_number, 100)

        expect_gradient_vector = np.array([0.0, 0.0])
        for element_number in range(self.statesSpace.element_count):
            gradient_vector = self.statesSpace.get_gradient(element_number)
            self.assertEqual(gradient_vector.tolist(), expect_gradient_vector.tolist())


if __name__ == "__main__":
    unittest.main()
