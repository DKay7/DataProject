import pandas as pd


def simple_output(data, *names): # several columns are expected
    output = data.drop(columns=names)
    return output


def statistic_output_for_str(data, *names): # one column is expected
    output = data[names[0]].value_counts().to_frame().rename(columns={name: 'Counts'})
    summ = output['Counts'].sum()
    output = output.assign(Percents=lambda x: x / summ * 100)
    return output


def statistic_output_for_values(data, *names): # one column is expected
    stat = data[names[0]]
    output = stat.to_frame().assign(Maximum='', Minimum='', Mean='', StandartDeviation='', Variance='')
    output.loc[0, 'Maximum'] = str(stat.max())
    output.loc[0, 'Minimum'] = str(stat.min())
    output.loc[0, 'Mean'] = str(stat.mean())
    output.loc[0, 'StandartDeviation'] = str(stat.std())
    output.loc[0, 'Variance'] = str(stat.var())
    return output


def pivot_output(data, *names): # two columns + aggfunc are expected
    output = pd.pivot_table(data, index=[names[0], names[1]], aggfunc=[names[2]])
    return output
