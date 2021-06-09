import pandas as pd
from loaders import data


def initialization():
    columns_number = data.shape[1]
    rows_number = data.shape[0]
    temp = dict.fromkeys(range(columns_number))
    i = 0
    for column in data.columns:
        temp[i] = column
        i += 1
    params = pd.DataFrame.from_dict(temp, orient='index')
    params['Options'] = pd.Series(0, index=params.index)
    params['Misc'] = pd.Series('', index=params.index)
    params = params.rename(columns={0: 'Name'})  
    return columns_number, rows_number, params


def simple_output(params):
    for_remove = []
    for i in params.index:
        if params['Options'][i] == 0:
            for_remove.append(params.at[i,'Name'])
    output = data.drop(columns=for_remove)
    return output


def statistic_output_for_str(params):
    for_stat = 0
    for i in params.index:
        if params['Options'][i]:
            for_stat = params['Name'][i]
    stat = data[for_stat].value_counts()
    output = stat.to_frame()
    output = output.rename(columns={'Country': 'Counts'})
    sum_ = 0

    for s in output['Counts']:
        sum_ += s

    percents = []

    for i in output.index:
        percents.append(output['Counts'][i] / sum_ * 100)

    output['Percents'] = pd.Series(percents, index=output.index)
    return output


def statistic_output_for_values(params):
    for_stat = 0

    for i in params.index:
        if params['Options'][i]:
            for_stat = params['Name'][i]

    stat = data[for_stat]
    output = stat
    max_ = stat.max()  # max value
    min_ = stat.min()  # min value
    mean = stat.mean()  # mean
    std = stat.std()  # standard derivation
    var = stat.var()  # variance
    stats = [max_, min_, mean, std, var]
    return output, stats


def pivot_output(params):
    for_stat = []
    for i in params.index:
        if params['Options'][i]:
            for_stat.append(params['Name'][i])

    output = pd.pivot_table(data, index=data.index, values=[for_stat])
    return output
