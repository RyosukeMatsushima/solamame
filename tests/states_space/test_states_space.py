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

    def test_get_neighbors_element_number(self):
        reference_axes = [
            {"name": "a0", "min_value": -1.2, "max_value": 1.2, "resolution": 10},
            {"name": "a1", "min_value": -1.8, "max_value": 2.1, "resolution": 10},
        ]

        for axis in reference_axes:
            self.statesSpace.add_axis(
                axis["name"], axis["min_value"], axis["max_value"], axis["resolution"]
            )

        self.statesSpace.create()

        # first element
        a0 = 0
        a1 = 0
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [None, a0 + 1],
            "a1": [None, elemet_number + self.statesSpace.axes[0].length],
        }
        self.assertEqual(result, expect)

        # last element
        a0 = self.statesSpace.axes[0].length - 1
        a1 = self.statesSpace.axes[1].length - 1
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [elemet_number - 1, None],
            "a1": [elemet_number - self.statesSpace.axes[0].length, None],
        }
        self.assertEqual(result, expect)

        a0 = 4
        a1 = 3
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [elemet_number - 1, elemet_number + 1],
            "a1": [
                elemet_number - self.statesSpace.axes[0].length,
                elemet_number + self.statesSpace.axes[0].length,
            ],
        }
        self.assertEqual(result, expect)

        a0 = 0
        a1 = 6
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [None, elemet_number + 1],
            "a1": [
                elemet_number - self.statesSpace.axes[0].length,
                elemet_number + self.statesSpace.axes[0].length,
            ],
        }
        self.assertEqual(result, expect)

        a0 = 9
        a1 = 0
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [elemet_number - 1, elemet_number + 1],
            "a1": [None, elemet_number + self.statesSpace.axes[0].length],
        }
        self.assertEqual(result, expect)

        a0 = (self.statesSpace.axes[0].length * 10) - 1
        a1 = 13
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [elemet_number - 1, None],
            "a1": [
                elemet_number - self.statesSpace.axes[0].length,
                elemet_number + self.statesSpace.axes[0].length,
            ],
        }
        self.assertEqual(result, expect)

        a0 = 12
        a1 = (self.statesSpace.axes[1].length * 10) - 1
        elemet_number = a0 + a1 * self.statesSpace.axes[0].length
        result = self.statesSpace.get_neighbors_element_number(elemet_number)
        expect = {
            "a0": [elemet_number - 1, elemet_number + 1],
            "a1": [elemet_number - self.statesSpace.axes[0].length, None],
        }
        self.assertEqual(result, expect)

    def test_save_and_read(self):
        reference_axes = [
            {"name": "a0", "min_value": -1.2, "max_value": 1.2, "resolution": 10},
            {"name": "a1", "min_value": -1.8, "max_value": 2.1, "resolution": 10},
        ]

        for axis in reference_axes:
            self.statesSpace.add_axis(
                axis["name"], axis["min_value"], axis["max_value"], axis["resolution"]
            )

        self.statesSpace.create()

        self.statesSpace.values = np.random.rand(self.statesSpace.element_count)

        values_before_save = self.statesSpace.values

        self.statesSpace.save(".")
        self.statesSpace.read(".")

        self.assertEqual(
            reference_axes[0]["min_value"], self.statesSpace.axes[0].min_value
        )
        self.assertTrue((values_before_save == self.statesSpace.values).all())


if __name__ == "__main__":
    unittest.main()
