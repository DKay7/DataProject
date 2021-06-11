from graphic.main_window import MainWindow
from tkinter import Tk


if __name__ == "__main__":
    root = Tk()
    main_window = MainWindow(root)
    main_window.start_main_loop()
