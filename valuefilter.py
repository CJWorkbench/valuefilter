import pandas as pd
import json


def value_filter(table, column, values, drop_or_keep):
    if column not in table.columns:
        return 'You chose a missing column'

    # delete values
    if drop_or_keep == 0:
        # NOP
        if len(values) == 0:
            return table
        return table[~table[column].astype(str).isin(values)].reset_index(drop=True)

    # keep values
    elif drop_or_keep == 1:
        return table[table[column].astype(str).isin(values)].reset_index(drop=True)

    return table


def render(table, params):
    column = params['column']
    valueselect = params['valueselect']
    drop_or_keep = params['drop_or_keep']
    values = json.loads(valueselect) if valueselect else []

    #NOP
    if not column or not values:
        return table

    return value_filter(table, column, values, drop_or_keep)
