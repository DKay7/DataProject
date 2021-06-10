from loaders import data
from graphic.main_window import MainWindow
from tkinter import Tk


if __name__ == "__main__":
    root = Tk()
    main_window = MainWindow(root, data)
    main_window.start_main_loop()
