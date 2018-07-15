import tkinter as tk
from tkinter import ttk

class AppUI(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Time Series")
        main_window.configure(width=500, height=400)


        self.place(relwidth=1, relheight=1)


main_window = tk.Tk()
app = AppUI(main_window)
app.mainloop()