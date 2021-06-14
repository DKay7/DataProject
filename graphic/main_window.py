import tkinter as tk
import pickle
import pandas as pd
import os
from tkinter import ttk, filedialog, Menu
from graphic.graphics_config import *
from graphic.edit_data_form import EditForm
from graphic.stats_forms import SimpleTextSubmissionForm, StatisticSubmissionForm, PivotSubmissionForm
from graphic.stats_forms import ClusteredBarPlotSubmitForm, CategorizedHistogramPlotSubmitForm
from graphic.stats_forms import BoxWhiskerPlotSubmitForm, ScatterPlotSubmitForm
from library.utils import get_types_list
from scripts.stat_text_submission_utils import simple_output, statistic_output, pivot_output
from scripts.stat_plot_submission_utils import bar_diagram, hist_diagram, box_diagram, scatter_diagram
from graphic.show_stats_window import TextStatShowWindow, PlotStatShowWindow


class MainWindow(tk.Frame):
    def __init__(self, root):
        self.root_frame = root
        self.df = None
        self.types = None
        tk.Frame.__init__(self,  self.root_frame)

        self.table_frame = self.get_main_window()
        self.table = None
        self.mouse_menu = None

        self.init_window()
        self.pack()

    def init_window(self):
        self.table = ttk.Treeview(self.table_frame)

        if self.df is not None and not isinstance(self.df.index, pd.MultiIndex):
            self.mouse_menu = self.get_table_mouse_menu()
            self.bind_events()
        else:
            self.mouse_menu = None

        self.add_main_menu()

    def add_df(self):
        self.init_window()

        if isinstance(self.df.index, pd.RangeIndex):
            headings = list(self.df.columns)
        else:
            headings = ["Индекс"] + list(self.df.columns)

        self.table['show'] = "headings"
        self.table["columns"] = headings

        for header in headings:
            self.table.heading(header, text=header)

        for index, row in self.df.iterrows():
            list_row = list(row)
            if isinstance(self.df.index, pd.RangeIndex):
                self.table.insert("", "end", text=index, values=list_row)
            else:
                self.table.insert("", "end", text=index, values=[index] + list_row)

        scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscroll=scrollbar_y.set)
        self.table.configure(xscroll=scrollbar_x.set)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar_y.grid(row=0, column=1, sticky="NSEW")
        scrollbar_x.grid(row=1, column=0, sticky="NSEW")

    def add_multiindex_df(self):
        self.init_window()

        headings = list(self.df.reset_index().columns)
        self.table["columns"] = headings[1:]

        self.table.heading("#0", text=headings[0])
        for header in headings[1:]:
            self.table.heading(header, text=header)

        for idx, df_selected in self.df.groupby(level=0):
            node = self.table.insert("", "end", text=str(idx), open=False)

            for idx_l1, _ in df_selected.groupby(level=1):
                self.table.insert(node, "end", values=[idx_l1]+list(self.df.loc[idx, idx_l1]))

        scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscroll=scrollbar_y.set)
        self.table.configure(xscroll=scrollbar_x.set)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar_y.grid(row=0, column=1, sticky="NSEW")
        scrollbar_x.grid(row=1, column=0, sticky="NSEW")

    def get_main_window(self):
        self.root_frame.title(WINDOW_TITLE)
        self.root_frame.geometry(WINDOW_DEFAULT_SIZES)
        self.root_frame.minsize(*WINDOW_MIN_SIZES)

        table_frame = tk.Frame(self.root_frame)
        table_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        return table_frame

    def add_main_menu(self):
        mainmenu = Menu(self.root_frame)
        self.root_frame.config(menu=mainmenu)

        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Открыть...", command=self.open_file_button_action)

        mainmenu.add_cascade(label="Файл",
                             menu=filemenu)

        if self.table.get_children():
            filemenu.add_command(label="Сохранить...", command=self.save_file_button_action)

            if self.df is not None and not isinstance(self.df.index, pd.MultiIndex):
                filemenu.add_command(label="Добавить новую запись в таблицу", command=self.add_table_entry)

                stats_menu = Menu(mainmenu, tearoff=0)
                stats_menu.add_command(label="Простой текстовый отчет",
                                       command=self.prepare_simple_text_stat_submission)
                stats_menu.add_command(label="Текстовый статистический отчет",
                                       command=self.prepare_text_stat_submission)
                stats_menu.add_command(label="Сводная таблица",
                                       command=self.prepare_pivot_table)
                stats_menu.add_command(label="Кластеризованная столбчатая диаграмма",
                                       command=self.prepare_clustered_bar_plot)
                stats_menu.add_command(label="Категоризированная гистограмма",
                                       command=self.prepare_categorized_histogram)
                stats_menu.add_command(label="Категоризированная диаграмма Бокса-Вискера",
                                       command=self.prepare_box_whiskers_diagram)
                stats_menu.add_command(label="Категоризированная диаграмма рассеивания",
                                       command=self.prepare_scatter_plot)

                mainmenu.add_cascade(label="Статистика",
                                     menu=stats_menu)

    def prepare_simple_text_stat_submission(self):
        window = SimpleTextSubmissionForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        result_df = simple_output(self.df, result)
        TextStatShowWindow(self.root_frame, result_df)
        print("Простой текстовый отчет\n", result_df)

    def prepare_text_stat_submission(self):
        # TODO make it!
        window = StatisticSubmissionForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        result_df = statistic_output(self.df, result)
        TextStatShowWindow(self.root_frame, result_df)
        print("Текстовый отчет\n", result_df.head())

    def prepare_pivot_table(self):
        # TODO make it!
        window = PivotSubmissionForm(self.root_frame, self.df)
        result, agg_func = window.open()

        if not result:
            return

        result_df = pivot_output(self.df, *result, agg_func=agg_func)

        TextStatShowWindow(self.root_frame, result_df)
        print("Сводная таблица\n", result_df.head())

    def prepare_clustered_bar_plot(self):
        # TODO make it!
        window = ClusteredBarPlotSubmitForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        figure = bar_diagram(self.df, result)
        PlotStatShowWindow(self.root_frame, figure)

        print("Столбчатая диаграмма\n", result)

    def prepare_categorized_histogram(self):
        # TODO make it!
        window = CategorizedHistogramPlotSubmitForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        figure = hist_diagram(self.df, result)
        PlotStatShowWindow(self.root_frame, figure)

        print("Гистограмма\n", result)

    def prepare_box_whiskers_diagram(self):
        # TODO make it!
        window = BoxWhiskerPlotSubmitForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        figure = box_diagram(self.df, result)
        PlotStatShowWindow(self.root_frame, figure)

        print("Диаграмма бокса-вискера\n", result)

    def prepare_scatter_plot(self):
        # TODO make it!
        window = ScatterPlotSubmitForm(self.root_frame, self.df)
        result = window.open()

        if not result:
            return

        figure = scatter_diagram(self.df, result)
        PlotStatShowWindow(self.root_frame, figure)

        print("Диаграмма рассеивания\n", result)

    def bind_events(self):
        self.table.bind("<Button-3>", self.post_mouse_menu)

    def get_table_mouse_menu(self):
        mouse_menu = Menu(self.table, tearoff=0)
        mouse_menu.add_command(label="Редактировать запись",
                               command=self.edit_table_entry)
        mouse_menu.add_separator()
        mouse_menu.add_command(label="Удалить запись",
                               command=self.delete_table_entry)

        return mouse_menu

    def post_mouse_menu(self, event):
        if self.table.focus():
            self.mouse_menu.post(event.x_root, event.y_root)

    def save_file_button_action(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".kek",
                                                filetypes=[('DP files', '*.kek')])

        if not filepath:
            return

        with open(filepath, mode="wb") as file:
            pickle.dump(self.df, file)

    def open_file_button_action(self):
        filepath = filedialog.askopenfilename(initialdir=r"./data/",
                                              defaultextension='.kek',
                                              filetypes=[('DP files', '*.kek'),
                                                         ('CSV files', '*.csv')])

        if not filepath:
            return

        filename, file_extension = os.path.splitext(filepath)

        if file_extension == '.csv':
            with open(filename+'.kek', 'wb') as file:
                data = pd.read_csv(filepath)
                self.types = get_types_list(data)
                pickle.dump(data, file)
                filepath = filename + '.kek'
                print("File saved as a bytes file")

        with open(filepath, 'rb') as file:
            self.df = pickle.load(file)

        if isinstance(self.df.index, pd.MultiIndex):
            self.add_multiindex_df()
        else:
            self.add_df()

        self.add_main_menu()

    def add_table_entry(self):
        columns = list(self.df.columns)
        values = [None] * len(columns)

        fields = list(zip(columns, values))

        form = EditForm(self.root_frame, fields, "Добавить новую запись в таблицу")
        result = form.open()

        self.df.loc[len(self.df.index)] = result
        self.table.insert("", "end", text=len(self.df.index), values=result)

    def edit_table_entry(self):
        item_id = self.table.selection()[0]
        item_dict = self.table.item(item_id)
        index = item_dict['text']

        columns = list(self.df.columns)
        values = self.table.item(item_id)['values']
        values += [""] * max(0, (len(columns) - len(values)))

        fields = list(zip(columns, values))

        form = EditForm(self.root_frame, fields, "Редактировать значение")
        result = form.open()

        self.df.iloc[index] = result
        self.table.item(item_id, values=result)

    def delete_table_entry(self):
        selected_item = self.table.selection()[0]
        self.table.delete(selected_item)

    def start_main_loop(self):
        self.root_frame.mainloop()
