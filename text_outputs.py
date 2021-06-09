import pandas as pd
data = pd.read_csv('D:\\base\International_Astronaut_Database.csv')


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
    return(columns_number, rows_number, params)


def simple_output(params):
    for_remove = []
    for i in params.index:
        if params['Options'][i] == 0:
            for_remove.append(params.at[i,'Name'])
    output = data.drop(columns=for_remove)
    return(output)


def statistic_output_for_str(params):
    for i in params.index:
        if params['Options'][i]:
            for_stat = params['Name'][i]
    stat = data[for_stat].value_counts()
    output = stat.to_frame()
    output = output.rename(columns={'Country': 'Counts'})
    sum = 0
    for s in output['Counts']:
        sum += s
    percents = []
    for i in output.index:
        percents.append(output['Counts'][i] / sum * 100)
    output['Percents'] = pd.Series(percents, index=output.index)
    return(output)


def statistic_output_for_values(params):
    for i in params.index:
       if params['Options'][i]:
           for_stat = params['Name'][i]
    stat = data[for_stat]
    output = stat
    max = stat.max() # максимум
    min = stat.min() # минимум
    mean = stat.mean() # среднее арифметическое
    std = stat.std() # стандартное отклонение
    var = stat.var() # выборочная дисперсия
    stats = [max, min, mean, std, var]
    return(output, stats)


def pivot_output(params):
    for_stat = []
    for i in params.index:
       if params['Options'][i]:
           for_stat.append(params['Name'][i])
    output = pd.pivot_table(data, index = data.index, values = [for_stat])
    return(output)
