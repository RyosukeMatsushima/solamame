import unittest

from modules.states_space.axis import Axis


class AxisTest(unittest.TestCase):
    def test_init(self):
        def check():
            axis = Axis(name, min_value, max_value, resolution)

            self.assertEqual(expect_min_value, axis.min_value)
            self.assertEqual(expect_max_value, axis.max_value)
            self.assertEqual(expect_length, axis.length)

        name = "test"
        min_value = -1.0
        max_value = 1.0
        resolution = 4

        expect_min_value = -1.0
        expect_max_value = 1.0
        expect_length = 2 * 4 + 1

        check()

        min_value = -3.3
        max_value = 23.1
        resolution = 4

        expect_min_value = -3.5
        expect_max_value = 23.25
        expect_length = 26 * 4 + 3 + 1

        check()

        # TODO: add only positive or negative range.

    def test_get_value(self):
        def check():
            axis = Axis(name, min_value, max_value, resolution)

            self.assertEqual(expect_value, axis.get_value(point))

        name = "test"
        min_value = -2.4
        max_value = 1.2
        resolution = 5

        point = 5
        expect_value = -1.4

        check()

        """
        point     0   1   2   3   4   5   6   7   8
                  *   *   *   *   *   *   *   *   *  ....
                  |       |           |        |
        value   -2.4    -2.0        -1.4    -1.0
        """

    # TODO: add only positive or negative range.

    def test_get_point(self):
        def check():
            axis = Axis(name, min_value, max_value, resolution)

            self.assertEqual(expect_point, axis.get_point(value))

        name = "test"
        min_value = -3.5
        max_value = 0.3
        resolution = 3

        value = -2.9
        expect_point = 2

        check()

        """
        point     0   1   2   3   4   5   6   7   8
                  *   *   *   *   *   *   *   *   *   *  ....
                  |       |           |           |
        value   -3.6    -3.0        -2.0        -1.0
        """

        min_value = -3.5
        max_value = 0.3
        resolution = 3

        value = -3.4
        expect_point = 1

        check()

        # TODO: add only positive or negative range.
