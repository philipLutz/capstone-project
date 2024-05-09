"""
Unit tests for scripting functions
"""

import unittest

from score_program_performance import order_of_magnitude, compute_score
from collect_program_data import collect_static_metrics
# from collect_performance_data import format_perf_stat, format_cpudist


class TestAllFunctions(unittest.TestCase):

    def test_order_of_magnitude(self):
        self.assertEqual(order_of_magnitude(0.0), 0)
        for i in range(10):
            self.assertEqual(order_of_magnitude(1.0 * (10 ** i)), i)
            self.assertEqual(order_of_magnitude(1.0 * (10 ** -i)), -i)

    def test_compute_score(self):
        # (cache-miss-percent / instructions-per-cycle) * (most_frequent_block_time + max_block_time)
        # most_frequent_block_time == '0-31'
        # max_block_time == '512-1023'
        fake_score = (0.5 / 2.1) * (15.5 + 767.5)
        test_run = {
            'program': 'thing',
            'cache-misses-percent': '0.5',
            'context-switches': '100',
            'instructions-per-cycle': '2.1',
            'elapsed': '5.0',
            'user': '1.0',
            'sys': '3.0',
            '0-31': '100',
            '32-63': '1',
            '64-127': '1',
            '128-255': '0',
            '256-511': '0',
            '512-1023': '1',
            '1024-2047': '0',
            '2048-4095': '0',
            '4096-8191': '0',
            '8192-16383': '0',
            '16384-32767': '0',
            '32768-65535': '0',
            '65536-131071': '0',
        }
        self.assertEqual(order_of_magnitude(fake_score), order_of_magnitude(compute_score(test_run)))

    def test_collect_static_metrics(self):
        expect_dict = {
            'max-cyclomatic-complexity': 3,
            'loops': 2,
            'assignments': 13,
            'function-calls': 54,
            'sum-cyclomatic-complexity': 5,
            'total-operators': 643,
            'distinct-operators': 61,
            'total-operands': 358,
            'distinct-operands': 209,
            'input-output': 30,
            'file-position': 5,
            'dynamic-memory-calls': 4,
            'file-access': 6,
            'file-operation': 4,
            'file-error': 3,
        }
        result_dict = collect_static_metrics("test-programs/add/add.c")
        for k in expect_dict.keys():
            self.assertEqual(expect_dict[k], result_dict[k])

    # def test_format_perf_stat(self):


    # def test_format_cpudist(self):




if __name__ == '__main__':
    unittest.main()
