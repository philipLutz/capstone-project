"""
Unit tests for scripting functions
"""

import unittest
import math

from score_program_performance import order_of_magnitude, compute_score


class TestAllFunctions(unittest.TestCase):

    def test_order_of_magnitude(self):
        self.assertEqual(order_of_magnitude(0.0), 0)
        for i in range(10):
            self.assertEqual(order_of_magnitude(1.0 * (10 ** i)), i)
            self.assertEqual(order_of_magnitude(1.0 * (10 ** -i)), -i)

    def test_compute_score(self):
        print('hi')



if __name__ == '__main__':
    unittest.main()
