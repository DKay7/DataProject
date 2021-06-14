import pandas as pd
from library.utils import separate_columns


def simple_output(data, names):  # zero, one or several columns are expected
    output = data.drop(columns=names)
    return output


def statistic_output(data, name):  # one column is expected
    column = data[name]

    qualitative, quantitative = separate_columns(data)
    if column.name in tuple(quantitative):
        output = pd.DataFrame()
        output = output.assign(Maximum='', Minimum='', Mean='', StandardDeviation='', Variance='')
        output.loc[0, 'Maximum'] = str(column.max())
        output.loc[0, 'Minimum'] = str(column.min())
        output.loc[0, 'Mean'] = str(column.mean())
        output.loc[0, 'StandardDeviation'] = str(column.std())

        try:
            output.loc[0, 'Variance'] = str(column.var())
        except TypeError:
            output.loc[0, 'Variance'] = "Не определено"

        output = output.set_index(pd.Index([str(column.name)]))
        return output

    else:

        output = pd.DataFrame()
        output = output.assign(Counts=column.value_counts())
        sum_ = output['Counts'].sum()
        output = output.assign(Percents=lambda x: x / sum_ * 100)

        return output


def pivot_output(data, *names, agg_func):  # two columns + agg_func are expected
    assert len(names) == 2
    output = pd.pivot_table(data, index=names, aggfunc=agg_func)
    return output
