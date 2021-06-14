import pickle
import pandas as pd
import tkinter as tk
from tkinter import Toplevel, ttk, Menu, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TextStatShowWindow(Toplevel):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df
        self.table = ttk.Treeview(self)
        self.add_main_menu()

        if isinstance(df.index, pd.MultiIndex):
            self.add_multiindex_df()
        else:
            self.add_df()

    def add_multiindex_df(self):
        headings = list(self.df.reset_index().columns)
        self.table["columns"] = headings[1:]

        self.table.heading("#0", text=headings[0])
        for header in headings[1:]:
            self.table.heading(header, text=header)

        for idx, df_selected in self.df.groupby(level=0):
            node = self.table.insert("", "end", text=str(idx), open=False)

            for idx_l1, _ in df_selected.groupby(level=1):
                self.table.insert(node, 0, values=[idx_l1]+list(self.df.loc[idx, idx_l1].values))

        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscroll=scrollbar_y.set)
        self.table.configure(xscroll=scrollbar_x.set)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar_y.grid(row=0, column=1, sticky="NSEW")
        scrollbar_x.grid(row=1, column=0, sticky="NSEW")

    def add_df(self):
        if isinstance(self.df.index, pd.RangeIndex):
            headings = list(self.df.columns)
        else:
            headings = ["Индекс"] + list(self.df.columns)

        self.table['show'] = "headings"
        self.table["columns"] = headings

        for header in tuple(headings):
            self.table.heading(header, text=header)

        for index, row in self.df.iterrows():
            list_row = list(row)
            if isinstance(self.df.index, pd.RangeIndex):
                self.table.insert("", "end", text=index, values=list_row)
            else:
                self.table.insert("", "end", text=index, values=[index] + list_row)

        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscroll=scrollbar_y.set)
        self.table.configure(xscroll=scrollbar_x.set)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar_y.grid(row=0, column=1, sticky="NSEW")
        scrollbar_x.grid(row=1, column=0, sticky="NSEW")

    def add_main_menu(self):
        mainmenu = Menu(self)
        filemenu = Menu(mainmenu, tearoff=0)

        self.config(menu=mainmenu)
        filemenu.add_command(label="Сохранить...", command=self.save_file_button_action)
        mainmenu.add_cascade(label="Файл", menu=filemenu)

    def save_file_button_action(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".kek",
                                                filetypes=[('DP files', '*.kek')])

        if not filepath:
            return

        with open(filepath, mode="wb") as file:
            pickle.dump(self.df, file)


class PlotStatShowWindow(Toplevel):
    def __init__(self, parent, fig):
        super().__init__(parent)

        self.resizable(0, 0)
        self.fig = fig
        self.add_plot()
        self.add_main_menu()

    def add_plot(self):
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=0.8)


    def add_main_menu(self):
        mainmenu = Menu(self)
        filemenu = Menu(mainmenu, tearoff=0)

        self.config(menu=mainmenu)
        filemenu.add_command(label="Сохранить...", command=self.save_file_button_action)
        mainmenu.add_cascade(label="Файл", menu=filemenu)

    def save_file_button_action(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[('DP Graph files', '*.png')])

        if not filepath:
            return

        self.fig.savefig(filepath)
