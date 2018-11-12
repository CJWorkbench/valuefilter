import pandas as pd
import json


def value_filter(table, column, values, drop_or_keep):
    if column not in table.columns:
        return 'You chose a missing column'

    # delete values
    if drop_or_keep == 0:
        return table[table[column].astype(str).isin(values)].reset_index(drop=True)

    # keep values
    elif drop_or_keep == 1:
        return table[~table[column].astype(str).isin(values)].reset_index(drop=True)

    return table


def render(table, params):
    column = params['column']
    valueselect = params['valueselect']
    drop_or_keep = params['drop_or_keep']
    if not column:
        return table

    if not valueselect:
        values = []
    else:
        values = json.loads(valueselect)['blacklist']

    return value_filter(table, column, values, drop_or_keep)
