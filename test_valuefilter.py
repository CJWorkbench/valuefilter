from dataclasses import dataclass
import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from valuefilter import value_filter, render, migrate_params

@dataclass(frozen=True)
class Column:
    name: str
    type: str


class MigrateParamsTests(unittest.TestCase):
    def test_v0_empty_valueselect(self):
        result = migrate_params({
            'column': 'A',
            'valueselect': '',
            'drop_or_keep': 1,
        })
        self.assertEqual(result, {
            'column': 'A',
            'valueselect': [],
            'drop': False,
        })

    def test_v0_keep(self):
        result = migrate_params({
            'column': 'A',
            'valueselect': '["foo", "bar"]',
            'drop_or_keep': 0,
        })
        self.assertEqual(result, {
            'column': 'A',
            'valueselect': ['foo', 'bar'],
            'drop': True,
        })

    def test_v1(self):
        result = migrate_params({
            'column': 'A',
            'valueselect': ['foo', 'bar'],
            'drop': True,
        })
        self.assertEqual(result, {
            'column': 'A',
            'valueselect': ['foo', 'bar'],
            'drop': True,
        })


class ValueFilterTests(unittest.TestCase):
    def test_keep_string(self):
        result = pd.DataFrame({
            'A': ['apple', 'apple', 'orange'],
            'B': ['monkey', 'kangaroo', 'cat'],
        })
        result = value_filter(result, 'A', ['apple'], False)
        expected = pd.DataFrame({
            'A': ['apple', 'apple'],
            'B': ['monkey', 'kangaroo'],
        })
        assert_frame_equal(result, expected)

    def test_keep_string_with_categories(self):
        result = pd.DataFrame({
            'A': ['apple', 'apple', 'orange'],
            'B': ['monkey', 'kangaroo', 'cat'],
        }, dtype='category')
        result = value_filter(result, 'A', ['apple'], False)
        expected = pd.DataFrame({
            'A': ['apple', 'apple'],
            'B': ['monkey', 'kangaroo'],
        }, dtype='category')
        assert_frame_equal(result, expected)

    def test_drop_string(self):
        result = pd.DataFrame({
            'A': ['apple', 'apple', 'orange'],
            'B': ['monkey', 'kangaroo', 'cat'],
        })
        result = value_filter(result, 'A', ['apple'], True)
        expected = pd.DataFrame({'A': ['orange'], 'B': ['cat']})
        assert_frame_equal(result, expected)

    def test_keep_drops_na(self):
        result = pd.DataFrame({'A': ['a', None, 'b']})
        result = value_filter(result, 'A', ['a'], False)
        expected = pd.DataFrame({'A': ['a']})
        assert_frame_equal(result, expected)

    def test_drop_keeps_na(self):
        result = pd.DataFrame({'A': ['a', None, 'b']})
        result = value_filter(result, 'A', ['a'], True)
        expected = pd.DataFrame({'A': [None, 'b']})
        assert_frame_equal(result, expected)

class RenderTest(unittest.TestCase):
    def test_no_colnames(self):
        # No colnames -> do nothing
        result = pd.DataFrame({'A': ['', np.nan, 'x']})
        result = render(result,
                        {'column': '', 'valueselect': [], 'drop': True},
                        input_columns={'A': Column('A', 'text')})
        expected = pd.DataFrame({'A': ['', np.nan, 'x']})
        assert_frame_equal(result, expected)

    def test_no_values(self):
        # Drop with valueselect = empty array
        result = pd.DataFrame({'A': ['', np.nan, 'x']})
        result = render(result,
                        {'column': 'A', 'valueselect': [], 'drop': False},
                        input_columns={'A': Column('A', 'text')})
        expected = pd.DataFrame({'A': ['', np.nan, 'x']})
        assert_frame_equal(result, expected)

    def test_not_text_is_error(self):
        result = render(pd.DataFrame({'A': [1, 2]}),
                        {'column': 'A', 'valueselect': ['1'], 'drop': True},
                        input_columns={'A': Column('A', 'number')})
        self.assertEqual(result,
                         'Please convert this column to Text first.')


if __name__ == '__main__':
    unittest.main()
