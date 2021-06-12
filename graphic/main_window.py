import tkinter as tk
import pickle
from tkinter import ttk, filedialog, Menu
from graphic.graphics_config import *
from graphic.edit_data_form import EditForm
from graphic.stats_forms import TextSubForm
from graphic.stats_forms import ChooseVariablesForm


class MainWindow(tk.Frame):
    def __init__(self, root):
        self.root_frame = root
        self.df = None
        tk.Frame.__init__(self,  self.root_frame)

        self.table_frame = self.get_main_window()
        self.table = ttk.Treeview(self.table_frame, show='headings')
        self.mouse_menu = self.get_table_mouse_menu()

        self.bind_events()
        self.add_main_menu()
        self.pack()

    def add_df(self):
        self.table.delete(*self.table.get_children())

        self.table["columns"] = tuple(self.df.columns)

        for header in tuple(self.df.columns):
            self.table.heading(header, text=header)

        for index, row in self.df.iterrows():
            tuple_row = tuple(row)

            self.table.insert("", "end", text=index, values=tuple_row)

        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="NSEW")

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

        if self.table.get_children():
            filemenu.add_command(label="Сохранить...", command=self.save_file_button_action)
            filemenu.add_command(label="Добавить новую запись в таблицу", command=self.add_table_entry)

            stats_menu = Menu(mainmenu, tearoff=0)
            stats_menu.add_command(label="Простой текстовый отчет",
                                   command=self.prepare_simple_text_stat_submission)
            stats_menu.add_command(label="Текстовый статистический отчет",
                                   command=self.prepare_text_stat_submission)
            stats_menu.add_command(label="Сводная таблица",
                                   command=self.prepare_summary_table)
            stats_menu.add_command(label="Кластеризованная столбчатая диаграмма",
                                   command=self.prepare_clustered_bar_plot)
            stats_menu.add_command(label="Категоризированная гистограмма",
                                   command=self.prepare_categorized_histogram)
            stats_menu.add_command(label="Категоризированная диаграмма Бокса-Вискера",
                                   command=self.prepare_box_whiskers_diagram)
            stats_menu.add_command(label="Категоризированная диаграмма рассеивания",
                                   command=self.prepare_scatter_plot)

            mainmenu.add_cascade(label="Файл",
                                 menu=filemenu)

            mainmenu.add_cascade(label="Статистика",
                                 menu=stats_menu)
        else:
            mainmenu.add_cascade(label="Файл",
                                 menu=filemenu)

    def prepare_simple_text_stat_submission(self):
        # TODO make it!
        print("Простой текстовый отчет")

    def prepare_text_stat_submission(self):
        # TODO make it!
        window = TextSubForm(self.root_frame, tuple(self.df.columns))
        result = window.open()

        if not result:
            return

        # TODO proceed text submit
        window = ChooseVariablesForm(self.root_frame, tuple(self.df.columns))
        result = window.open()
        print("Текстовый отчет", result)

    def prepare_summary_table(self):
        # TODO make it!
        print("Сводная таблица")

    def prepare_clustered_bar_plot(self):
        # TODO make it!
        print("Столбчатая диаграмма")

    def prepare_categorized_histogram(self):
        # TODO make it!
        print("Гистограмма")

    def prepare_box_whiskers_diagram(self):
        # TODO make it!
        print("Диаграмма бокса-вискера")

    def prepare_scatter_plot(self):
        # TODO make it!
        print("Диаграмма рассеивания")

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
        try:
            with filedialog.asksaveasfile(mode='wb', defaultextension=".kek") as file:
                if file is None:
                    return

                pickle.dump(self.df, file)

        except AttributeError:
            return

    def open_file_button_action(self):
        try:
            with filedialog.askopenfile(mode="rb",
                                        initialdir=r"../data/",
                                        defaultextension='.kek',
                                        filetypes=[('DP-files files', '*.kek')]) as file:

                self.df = pickle.load(file)
                self.add_df()
                self.add_main_menu()
        except AttributeError:
            return

        print("File opened")

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

        values = self.table.item(item_id)['values']
        index = self.table.item(item_id)['text']
        columns = list(self.df.columns)

        values += [None] * max(0, (len(columns) - len(values)))
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
