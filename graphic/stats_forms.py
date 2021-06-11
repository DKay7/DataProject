import tkinter as tk
from tkinter import Toplevel, ttk


class ChooseVariablesForm(Toplevel):
    def __init__(self, parent, headings):
        super().__init__(parent)

        # TODO make it beautiful and universal!
        self.label1 = tk.Label(self, text="Первый параметр отчета")
        self.combobox1 = ttk.Combobox(self, values=headings)
        self.label2 = tk.Label(self, text="Второй параметр отчета")
        self.combobox2 = ttk.Combobox(self, values=headings)

        self.label1.grid(row=0, column=0)
        self.label2.grid(row=0, column=1)
        self.combobox1.grid(row=1, column=0)
        self.combobox2.grid(row=1, column=1)
        tk.Button(self, text="Подтвердить", command=self.destroy).grid(row=2, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

        # TODO some error here.
        # result = (self.combobox1.get(), self.combobox2.get())
        # return result
