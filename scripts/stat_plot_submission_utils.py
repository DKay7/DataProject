import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


def hist_diagram(data, names):
    assert len(names) == 2

    fig = Figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    g = data.groupby(data[names[0]])[names[1]].sum()
    ax.hist(data[names[0]], bins=g.size, weights=data[names[1]], label=g.index, color='teal')

    ax.tick_params(axis='x',
                   labelsize=7,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=5,
                   direction='out')

    ax.grid(which='major',
            color='darkcyan')

    return fig


def bar_diagram(df, names):
    assert len(names) == 2

    fig = Figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    ax.bar(df[names[0]], df[names[1]], color='teal')

    ax.tick_params(axis='x',
                   labelsize=7,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=5,
                   direction='out')

    return fig


def box_diagram(df, names):
    assert len(names) == 2

    fig = Figure(figsize=(7, 5))
    ax = fig.add_subplot(111)

    df.boxplot(ax=ax, by=names[0], column=names[1])

    ax.tick_params(axis='x',
                   labelsize=7,
                   direction='out',
                   labelrotation=90)

    ax.tick_params(axis='y',
                   labelsize=5,
                   direction='out')

    return fig


def scatter_diagram(df, names):
    assert len(names) == 3

    fig = Figure(figsize=(8, 9))
    ax = fig.add_subplot(111)

    df = pd.DataFrame(dict(x=df[names[0]], y=df[names[1]], label=df[names[2]]))

    groups = df.groupby('label')

    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=name)
    ax.legend(numpoints=1, loc='upper left')
    ax.set_xlabel(names[0])
    ax.set_ylabel(names[1])
    return fig
