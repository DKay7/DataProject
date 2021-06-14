import pandas as pd


def get_types_list(dataframe):
    flag = False
    name = ""

    for name in dataframe.columns:
        try:
            if len(dataframe[name][0].split(':')) == 3:
                flag = True
                break
        except AttributeError:
            pass

    if flag and name:
        time = []
        dataframe[name].apply(lambda x: x.split(':')).apply(
            lambda x: time.append(pd.Timedelta(days=int(x[0]), hours=int(x[1]), minutes=int(x[2]))))
        dataframe[name] = pd.Series(time)
        dataframe.rename(columns={name: 'Total Flight Time'}, inplace=True)

    types = dataframe.dtypes

    return types


def separate_columns(dataframe):

    quantitative = dataframe.select_dtypes(include=["number", "timedelta64[ns]"])
    qualitative = dataframe.select_dtypes(exclude=["number", "timedelta64[ns]"])

    return qualitative, quantitative
