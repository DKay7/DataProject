import pandas as pd


def get_types_list(dataframe):
    flag = False

    for name in dataframe.columns:
        try:
            if dataframe[name][0].split(':') == 3:
                flag = True
                break
        except AttributeError:
            pass

    if flag:
        time = []
        dataframe[name].apply(lambda x: x.split(':')).apply(
            lambda x: time.append(pd.Timedelta(days=int(x[0]), hours=int(x[1]), minutes=int(x[2]))))
        dataframe[name] = pd.Series(time)

    types = dataframe.dtypes

    return types
