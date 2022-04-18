import unittest
from waffle_solver import get_line_column


class TestWaffleSolver(unittest.TestCase):
    def test_get_line_column_line_and_column(self):
        self.assertEqual(get_line_column((0, 2)), [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                                   (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)])

    def test_get_line_column_line_only(self):
        self.assertEqual(get_line_column((2, 1)), [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)])

    def test_get_line_column_column_only(self):
        self.assertEqual(get_line_column((1, 2)), [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)])

