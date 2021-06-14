import pandas as pd


def simple_output(data, names):  # zero, one or several columns are expected
    output = data.drop(columns=names)
    return output


def statistic_output(data, name):  # one column is expected
    column = data[name]

    if column.name in tuple(data.select_dtypes(include="number")):
        output = pd.DataFrame()
        output = output.assign(Maximum='', Minimum='', Mean='', StandartDeviation='', Variance='')
        output.loc[0, 'Maximum'] = str(column.max())
        output.loc[0, 'Minimum'] = str(column.min())
        output.loc[0, 'Mean'] = str(column.mean())
        output.loc[0, 'StandartDeviation'] = str(column.std())
        output.loc[0, 'Variance'] = str(column.var())
        output.set_index(pd.Index([str(column.name)]))
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
