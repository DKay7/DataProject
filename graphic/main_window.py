import tkinter as tk
import pickle
from tkinter import ttk, filedialog, Menu
from graphic.graphics_config import *


class MainWindow(tk.Frame):
    def __init__(self, root, df):
        self.root_frame = root
        self.df = df
        tk.Frame.__init__(self,  self.root_frame)

        self.table_frame = self.get_main_window()
        self.table = ttk.Treeview(self.table_frame, show='headings')
        self.mouse_menu = self.get_table_mouse_menu()

        self.bind_events()
        self.add_main_menu()
        # self.add_df()
        self.pack()

    def add_df(self):
        self.table.delete(*self.table.get_children())

        self.table["columns"] = tuple(self.df.columns)

        for header in tuple(self.df.columns):
            self.table.heading(header, text=header)

        for index, row in self.df.iterrows():
            tuple_row = tuple(row)

            self.table.insert("", "end", values=tuple_row)

        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="EW")

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

            helpmenu = Menu(mainmenu, tearoff=0)
            helpmenu.add_command(label="Среднее арифметическое времени полетов")
            helpmenu.add_command(label="Еще какая-то статистика")

            mainmenu.add_cascade(label="Файл",
                                 menu=filemenu)

            mainmenu.add_cascade(label="Статистика",
                                 menu=helpmenu)
        else:
            mainmenu.add_cascade(label="Файл",
                                 menu=filemenu)

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
            with filedialog.askopenfile(mode="rb", filetypes=[('text files', '*.kek')]) as file:
                self.df = pickle.load(file)
                self.add_df()
                self.add_main_menu()
        except AttributeError:
            return

        print("File opened")

    def edit_table_entry(self):
        item_id = self.table.selection()
        item_values = self.table.item(item_id)["values"]
        print(item_values)

    def delete_table_entry(self):
        selected_item = self.table.selection()[0]
        self.table.delete(selected_item)

    def start_main_loop(self):
        self.root_frame.mainloop()
