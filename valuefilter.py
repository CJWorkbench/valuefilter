import pandas as pd
import json


def value_filter(table, column, values, drop):
    mask = table[column].isin(set(values))

    if drop:
        table = table[~mask]
    else:
        table = table[mask]

    table.reset_index(inplace=True, drop=True)
    for column in table.columns:
        if hasattr(table[column], 'cat'):
            table[column].cat.remove_unused_categories(inplace=True)
    return table


def render(table, params, *, input_columns):
    column = params['column']
    values = params['valueselect']

    if not column or not values:
        return table  # no-op

    if input_columns[column].type != 'text':
        return 'Please convert this column to Text first.'

    return value_filter(table, column, values, params['drop'])


def _migrate_params_v0_to_v1(params):
    """
    v0: params['valueselect'] is JSON, 'drop_or_keep' is 0(drop)/1(keep)

    v1: params['valueselect'] is Array of String values; 'drop' is bool
    """
    return {
        'column': params['column'],
        'valueselect': json.loads(params['valueselect'] or '[]'),
        'drop': params['drop_or_keep'] == 0,
    }


def migrate_params(params):
    if isinstance(params['valueselect'], str):
        params = _migrate_params_v0_to_v1(params)

    return params
