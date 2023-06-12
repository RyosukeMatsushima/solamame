import unittest

import numpy as np


class NumpyOperationCheck(unittest.TestCase):
    def test_argmax(self):
        a = np.array([[1, 4, 6], [0, 2, -1], [5, 34, 5], [-53, -2390, -4]])

        max_index = np.argmax(a, axis=0)

        expect = np.array([2, 2, 0])

        self.assertTrue(np.all(max_index == expect))

    def test_inner_product(self):
        a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        x = np.array([10, 20, 30])

        result = a @ x

        expect = np.array(
            [
                [
                    1 * 10 + 2 * 20 + 3 * 30,
                    4 * 10 + 5 * 20 + 6 * 30,
                    7 * 10 + 8 * 20 + 9 * 30,
                ]
            ]
        )

        self.assertTrue(np.all(result == expect))

    def test_numpy_choose(self):
        choices = [
            [0, 1, 2, 3],
            [10, 11, 12, 13],
            [20, 21, 22, 23],
            [30, 31, 32, 33],
            [40, 41, 42, 43],
        ]
        result = np.choose([2, 3, 1, 0], choices)
        expect = np.array([20, 31, 12, 3])

        self.assertTrue(np.all(result == expect))
