import matplotlib.pyplot as plt
import pandas as pd
import re
data = pd.read_csv('D:\\base\International_Astronaut_Database.csv')


def sort(flights):
    spaceships = []
    years = []
    for i in flights.index:
        temp = flights[i].split(',')
        for j in range(len(temp)):
            temp[j] = re.sub('\)', '', temp[j])
            temp[j] = re.sub(' ', '', temp[j])
            s = temp[j].split('(')
            spaceships.append(s[0])
            years.append(s[1])
    return(years, spaceships)


def bar_diagram(params):
    for i in params.index:
       if params['Options'][i]:
           if params['Misc'][i] == 'value':
               values = params['Name'][i]
           if params['Misc'][i] == 'label':
               labels = params['Name'][i]
    stat = data.groupby(data[labels])[values].sum()
    fig, ax = plt.subplots(figsize=(18, 7))
    ax.bar(stat.index, stat, color = 'r')
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.show()


# для отладки

temp = dict.fromkeys(range(data.shape[1]))
i = 0
for column in data.columns:
    temp[i] = column
    i += 1
params = pd.DataFrame.from_dict(temp, orient='index')
params['Options'] = pd.Series(0, index=params.index)
params['Misc'] = pd.Series('', index=params.index)
params = params.rename(columns={0: 'Name'})
params['Options'][1] = 1
params['Options'][4] = 1
params['Misc'][1] = 'label'
params['Misc'][4] = 'value'
stat = bar_diagram(params)