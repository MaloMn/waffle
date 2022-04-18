import unittest
from utils import words_to_grid_string


class TestUtilsFunctions(unittest.TestCase):
    def test_words_to_grid_string(self):
        self.assertEqual(words_to_grid_string(['AATUE', 'ELTBV', 'ROAAL', 'LOVIN', 'TIEIN', 'RAENT']),
                         'roaalaaoeltbvnuitiein'.upper())


if __name__ == '__main__':
    unittest.main()
