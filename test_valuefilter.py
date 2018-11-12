import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from valuefilter import value_filter, render


class TestRemoveDuplicates(unittest.TestCase):
    def test_delete_string(self):
        result = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': ['monkey', 'kangaroo', 'cat']})
        result = value_filter(result, 'A', ['apple'], 0)
        expected = pd.DataFrame({'A': ['apple', 'apple'], 'B': ['monkey', 'kangaroo']})
        assert_frame_equal(result, expected)

    def test_keep_string(self):
        result = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': ['monkey', 'kangaroo', 'cat']})
        result = value_filter(result, 'A', ['apple'], 1)
        expected = pd.DataFrame({'A': ['orange'], 'B': ['cat']})
        assert_frame_equal(result, expected)

    def test_delete_number(self):
        result = pd.DataFrame({'A': [1.0, 1.0, 2.3], 'B': ['monkey', 'kangaroo', 'cat']})
        result = value_filter(result, 'A', ['1.0'], 0)
        expected = pd.DataFrame({'A': [1.0, 1.0], 'B': ['monkey', 'kangaroo']})
        assert_frame_equal(result, expected)

    def test_keep_number(self):
        result = pd.DataFrame({'A': [1.0, 1.0, 2.3], 'B': ['monkey', 'kangaroo', 'cat']})
        result = value_filter(result, 'A', ['1.0'], 1)
        expected = pd.DataFrame({'A': [2.3], 'B': ['cat']})
        assert_frame_equal(result, expected)

class RenderTest(unittest.TestCase):
    def test_no_colnames(self):
        # No colnames -> do nothing
        result = pd.DataFrame({'A': ['', np.nan, 'x']})
        result = render(result,
                        {'column': '',
                         'valueselect': str('{"edits": "", "blacklist": []}'),
                         'drop_or_keep': 0
                        })
        expected = pd.DataFrame({'A': ['', np.nan, 'x']})
        assert_frame_equal(result, expected)


    def test_missing_colname(self):
        result = pd.DataFrame({'A': [1]})
        result = render(result,
                        {'column': 'B',
                         'valueselect': str('{"edits": "", "blacklist": []}'),
                         'drop_or_keep': 0
                         })
        self.assertEqual(result, 'You chose a missing column')


if __name__ == '__main__':
    unittest.main()
