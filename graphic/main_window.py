import tkinter as tk
from tkinter import ttk
from graphic.graphics_config import *


class MainWindow(tk.Frame):
    def __init__(self, root, df):
        self.root_frame = root
        self.df = df
        tk.Frame.__init__(self,  self.root_frame)

        self.menu_frame, self.table_frame = self.get_main_window()
        self.add_menu()
        self.add_df()

    def add_df(self):
        table = ttk.Treeview(self.table_frame, show='headings')
        table["columns"] = tuple(self.df.columns)

        for header in tuple(self.df.columns):
            table.heading(header, text=header)

        for index, row in self.df.iterrows():
            tuple_row = tuple(row)

            table.insert("", "end", values=tuple_row)

        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        table.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="NSEW")

    def get_main_window(self):
        self.root_frame.title(WINDOW_TITLE)
        self.root_frame.geometry(WINDOW_DEFAULT_SIZES)
        self.root_frame.minsize(*WINDOW_MIN_SIZES)

        menu_frame = tk.Frame(self.root_frame)
        table_frame = tk.Frame(self.root_frame)

        menu_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        table_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        return menu_frame, table_frame

    def add_menu(self):
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu_frame.columnconfigure(2, weight=1)

        self.menu_frame.rowconfigure(0, weight=2)
        self.menu_frame.rowconfigure(1, weight=1)

        menu_text = tk.Label(self.menu_frame, text="Меню",
                             font=MAIN_MENU_TITLE_TEXT_FONT, fg=MAIN_MENU_TEXT_COLOR)
        button_add_val = tk.Button(self.menu_frame, text="Добавить значение",
                                   command=self.add_val_button_action,
                                   font=MAIN_MENU_BUTTONS_TEXT_FONT,
                                   bg=MAIN_MENU_BUTTONS_BG_COLOR, fg=MAIN_MENU_TEXT_COLOR,
                                   activeforeground=MAIN_MENU_BUTTONS_BG_COLOR,
                                   activebackground=MAIN_MENU_TEXT_COLOR)

        button_del_val = tk.Button(self.menu_frame, text="Удалить значение",
                                   command=self.del_val_button_action,
                                   font=MAIN_MENU_BUTTONS_TEXT_FONT,
                                   bg=MAIN_MENU_BUTTONS_BG_COLOR, fg=MAIN_MENU_TEXT_COLOR,
                                   activeforeground=MAIN_MENU_BUTTONS_BG_COLOR,
                                   activebackground=MAIN_MENU_TEXT_COLOR)

        button_open_stats = tk.Button(self.menu_frame, text="Открыть статистику",
                                      command=self.open_stats_button_action,
                                      font=MAIN_MENU_BUTTONS_TEXT_FONT,
                                      bg=MAIN_MENU_BUTTONS_BG_COLOR, fg=MAIN_MENU_TEXT_COLOR,
                                      activeforeground=MAIN_MENU_BUTTONS_BG_COLOR,
                                      activebackground=MAIN_MENU_TEXT_COLOR)

        menu_text.grid(row=0, column=0, sticky='NSEW', columnspan=3)
        button_add_val.grid(row=1, column=0, sticky='NSEW')
        button_del_val.grid(row=1, column=1, sticky='NSEW')
        button_open_stats.grid(row=1, column=2, sticky='NSEW')

    def add_val_button_action(self):
        # TODO make it!
        print("val added")

    def del_val_button_action(self):
        # TODO make it!
        print("val deleted")

    def open_stats_button_action(self):
        # TODO make it!
        print("stats opened")

    def start_main_loop(self):
        self.root_frame.mainloop()
