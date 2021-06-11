import tkinter as tk
from tkinter import Toplevel


class EditForm(Toplevel):
    def __init__(self, parent, fields):
        super().__init__(parent)

        self.fields = list()

        for index, (column_name, old_value) in enumerate(fields):
            variable = tk.StringVar()

            label = tk.Label(self, text=column_name)
            entry = tk.Entry(self, textvariable=variable)
            entry.insert(0, str(old_value))

            label.grid(row=2, column=index+1)
            entry.grid(row=3, column=index+1)

            self.fields.append(variable)

        tk.Label(self, text="Изменить значение ячейки").grid(row=1, column=1, columnspan=len(self.fields))
        tk.Button(self, text="Подтвердить", command=self.destroy).grid(row=4, column=1, columnspan=len(self.fields))

    def open(self):
        self.grab_set()
        self.wait_window()

        result_fields = list()

        for field in self.fields:
            content = field.get()
            result_fields.append(content)

        return result_fields
