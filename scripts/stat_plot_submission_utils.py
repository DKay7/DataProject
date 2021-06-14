from matplotlib.figure import Figure


def hist_diagram(data, *names):
    assert len(names) == 2

    fig = Figure(figsize=(26, 20))
    ax = fig.add_subplot(111)
    g = data.groupby(data[names[0]])[names[1]].sum()
    ax.hist(data[names[0]], bins=g.size, weights=data[names[1]], label=g.index, color='teal')

    ax.tick_params(axis='x',
                   labelsize=18,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=15,
                   direction='out')

    ax.grid(which='major',
            color='darkcyan')

    return fig


def bar_diagram(df, *names):
    assert len(names) == 2

    fig = Figure(figsize=(26, 20))
    ax = fig.add_subplot(111)
    ax.bar(df[names[0]], df[names[1]], color='teal')

    ax.tick_params(axis='x',
                   labelsize=18,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=15,
                   direction='out')

    return fig


def box_diagram(df, *names):
    assert len(names) == 2

    fig = Figure(figsize=(26, 20))
    ax = fig.add_subplot(111)
    df.boxplot(ax=ax, column=names[0], by=names[1])

    ax.tick_params(axis='x',
                   labelsize=18,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=15,
                   direction='out')

    return fig


def scatter_diagram(df, *names):
    assert len(names) == 3
    pass

