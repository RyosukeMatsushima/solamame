import unittest

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


if __name__ == "__main__":
    unittest.main()
