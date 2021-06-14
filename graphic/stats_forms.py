import tkinter as tk
import numpy as np
from tkinter import Toplevel, ttk
from tkinter.messagebox import showerror
from library.utils import separate_columns


class SimpleTextSubmissionForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        self.variables = list()
        self.headings = tuple(df.columns)

        for index, heading in enumerate(self.headings):
            var = tk.StringVar()
            check_button = tk.Checkbutton(self, text=heading, variable=var,
                                          onvalue=heading, offvalue="")

            check_button.grid(row=1, column=index, sticky="EW")
            self.variables.append(var)

        tk.Label(self, text="Выберите столбец, по которому будет составлен отчет").grid(row=0, column=0,
                                                                                        columnspan=len(self.headings),
                                                                                        sticky="N")
        tk.Button(self, text="Подтвердить", command=self.destroy).grid(row=2, column=1,
                                                                       columnspan=len(self.headings),
                                                                       sticky="S")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list(map(lambda var: var.get(), self.variables))
        result = list(filter(None, result))

        if not result:
            showerror(title="Ошибка!", message="Выберите столбец")
            return False

        # Here we're finding columns to delete from df (all columns minus chosen columns)
        result = list(set(self.headings) - set(result))

        if not result:
            showerror(title="Ошибка!", message="Такой отчет идентичен исходной таблице")
            return False

        return result


class StatisticSubmissionForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        label = tk.Label(self, text="Выберите столбец, по которому будет составлен отчет")
        self.variable = tk.StringVar()
        combobox = ttk.Combobox(self, values=tuple(df.columns), textvariable=self.variable)
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        combobox.grid(row=1, column=0, )
        button.grid(row=1, column=1,)

    def open(self):
        self.grab_set()
        self.wait_window()

        result = self.variable.get()

        if not result:
            showerror(title="Ошибка!", message="Выберите столбец")
            return False

        return result


class PivotSubmissionForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        self.variables = list()
        self.agg_methods = {
            "сумма": np.sum,
            "среднее": np.mean,
            "медиана": np.median,
            "максимум": np.max,
            "минимум": np.min,
            "стандартное отклонение": np.std
        }

        qualitative_cols, _ = separate_columns(df)
        cols = tuple([tuple(qualitative_cols), tuple(qualitative_cols), tuple(self.agg_methods.keys())])
        labels = tuple(["1-й Качественный параметр", "2-й Качественный параметр",
                        "Метод агрегации"])

        for index, col in enumerate(cols):
            variable = tk.StringVar()
            combobox = ttk.Combobox(self, values=col, textvariable=variable)
            label = tk.Label(self, text=labels[index])

            self.variables.append(variable)

            combobox.grid(row=2, column=index)
            label.grid(row=1, column=index)

        label = tk.Label(self, text="Выберите два столбца, по которым будет составлен отчет. "
                                    "Выберите метод агрегации.")
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=3, sticky="NSEW")
        button.grid(row=3, column=0, columnspan=3, sticky="NSEW")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list()
        for variable in self.variables:
            value = variable.get()
            if value not in result:
                result.append(value)
            else:
                showerror(title="Ошибка!", message="Укажите уникальные столбцы")
                return False

        if not all(result):
            showerror(title="Ошибка!", message="Укажите данные во всех столбцах")
            return False

        return result[:-1], self.agg_methods[result[-1]]


class ClusteredBarPlotSubmitForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        qualitative_cols, _ = separate_columns(df)
        cols = tuple([tuple(qualitative_cols), tuple(qualitative_cols)])
        self.variables = list()

        for index, col in enumerate(cols):
            variable = tk.StringVar()
            combobox = ttk.Combobox(self, values=col, textvariable=variable)
            label = tk.Label(self, text=f"{index+1}й - качественный параметр")

            self.variables.append(variable)

            combobox.grid(row=2, column=index)
            label.grid(row=1, column=index)

        label = tk.Label(self, text="Выберите два столбца, по которым будет построена столбчатая диаграмма")
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        button.grid(row=3, column=0, columnspan=2, sticky="NSEW")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list()
        for variable in self.variables:
            value = variable.get()
            if value not in result:
                result.append(value)
            else:
                showerror(title="Ошибка!", message="Укажите уникальные столбцы")
                return False

        if not all(result):
            showerror(title="Ошибка!", message="Выберите оба столбца")
            return False

        return result


class CategorizedHistogramPlotSubmitForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        qualitative_cols, quantitative_cols = separate_columns(df)
        cols = tuple([tuple(qualitative_cols), tuple(quantitative_cols)])
        labels = tuple(["Качественный параметр", "Количественный параметр"])
        self.variables = list()

        for index, col in enumerate(cols):
            variable = tk.StringVar()
            combobox = ttk.Combobox(self, values=col, textvariable=variable)
            label = tk.Label(self, text=labels[index])

            self.variables.append(variable)

            combobox.grid(row=2, column=index)
            label.grid(row=1, column=index)

        label = tk.Label(self, text="Выберите два столбца, по которым будет построена гистограмма")
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        button.grid(row=3, column=0, columnspan=2, sticky="NSEW")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list()
        for variable in self.variables:
            result.append(variable.get())

        if not all(result):
            showerror(title="Ошибка!", message="Выберите оба столбца")
            return False

        return result


class BoxWhiskerPlotSubmitForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        qualitative_cols, quantitative_cols = separate_columns(df)
        cols = tuple([tuple(qualitative_cols), tuple(quantitative_cols)])
        labels = tuple(["Качественный параметр", "Количественный параметр"])
        self.variables = list()

        for index, col in enumerate(cols):
            variable = tk.StringVar()
            combobox = ttk.Combobox(self, values=col, textvariable=variable)
            label = tk.Label(self, text=labels[index])

            self.variables.append(variable)

            combobox.grid(row=2, column=index)
            label.grid(row=1, column=index)

        label = tk.Label(self, text="Выберите два столбца, по которым будет построена диаграмма Бокса-Вискера")
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        button.grid(row=3, column=0, columnspan=2, sticky="NSEW")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list()
        for variable in self.variables:
            value = variable.get()
            if value not in result:
                result.append(value)
            else:
                showerror(title="Ошибка!", message="Укажите уникальные столбцы")
                return False

        if not all(result):
            showerror(title="Ошибка!", message="Укажите данные во всех столбцах")
            return False

        return result[:-1], self.agg_methods[result[-1]]


class ScatterPlotSubmitForm(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.resizable(0, 0)

        qualitative_cols, quantitative_cols = separate_columns(df)

        cols = tuple([tuple(quantitative_cols), tuple(quantitative_cols), tuple(qualitative_cols)])
        labels = tuple(["Первый количественный параметр",
                        "Второй количественный параметр",
                        "Качественный параметр"])

        self.variables = list()

        for index, col in enumerate(cols):
            variable = tk.StringVar()
            combobox = ttk.Combobox(self, values=col, textvariable=variable)
            label = tk.Label(self, text=labels[index])

            self.variables.append(variable)

            combobox.grid(row=2, column=index)
            label.grid(row=1, column=index)

        label = tk.Label(self, text="Выберите три столбца, по которым будет построена "
                                    "категоризированная диаграмма рассеивания")
        button = tk.Button(self, text="Подтвердить", command=self.destroy)

        label.grid(row=0, column=0, columnspan=3, sticky="NSEW")
        button.grid(row=3, column=0, columnspan=3, sticky="NSEW")

    def open(self):
        self.grab_set()
        self.wait_window()

        result = list()
        for variable in self.variables:
            result.append(variable.get())

        if not all(result):
            showerror(title="Ошибка!", message="Выберите оба столбца")
            return False

        return result

