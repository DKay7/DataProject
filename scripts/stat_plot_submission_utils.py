from matplotlib.figure import Figure
from loaders import data
import re


def sort(flights):
    spaceships = []
    years = []

    for index in flights.index:
        flights_array = flights[index].split(',')
        for j in range(len(flights_array)):
            flights_array[j] = re.sub(r'\)', '', flights_array[j])
            flights_array[j] = re.sub(r' ', '', flights_array[j])
            s = flights_array[j].split(r'(')
            spaceships.append(s[0])
            years.append(s[1])

    return years, spaceships


def bar_diagram(df, names):
    assert len(names) == 2

    fig = Figure(figsize=(6, 6))
    a = fig.add_subplot(111)
    a.bar(df[names[0]], df[names[1]], color='red')

    return fig
