import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter.messagebox import showerror


class TextSubForm(Toplevel):
    def __init__(self, parent, headings):
        super().__init__(parent)

        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()

        self.label1 = tk.Label(self, text="Первый параметр отчета")
        self.label2 = tk.Label(self, text="Второй параметр отчета")
        self.combobox1 = ttk.Combobox(self, values=headings, textvariable=self.field1)
        self.combobox2 = ttk.Combobox(self, values=headings, textvariable=self.field2)

        self.label1.grid(row=0, column=0)
        self.label2.grid(row=0, column=1)
        self.combobox1.grid(row=1, column=0)
        self.combobox2.grid(row=1, column=1)
        tk.Button(self, text="Подтвердить", command=self.destroy).grid(row=2, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

        result = (self.field1.get(), self.field2.get())

        if not all(result):
            showerror(title="Ошибка!", message="Поля не могут быть пустыми!")
            return False

        return result
