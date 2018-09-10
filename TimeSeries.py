import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
style.use("ggplot")

import requests
import pandas as pd
import numpy as np
import datetime

f = Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(111)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("epppa")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10, padx=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


class TimeSeries(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        label = tk.Label(self, text=(
            """Bienvenido a la aplicacion de analisis de datos"""))
        label.grid(row=0, column=0)
        self.InitUi()

    def InitUi(self):
        self.label = ttk.Label(self, text="Seleccione su ticket")
        self.label.grid(row=1, column=0)

        self.ticket = tk.StringVar()
        self.combo = ttk.Combobox(
            self, width=15, textvariable=self.ticket, state='readonly')
        self.combo['values'] = ("AAPL", "MSFT", "AMZN", "GOOG", "ORCL")
        self.combo.current(2)
        self.combo.grid(row=2, column=0)

        self.button = ttk.Button(self, text="Click me", command=self.clickMe)
        self.button.grid(row=3, column=0)

    def clickMe(self):
        a.clear()
        self.canvasPlot()

    def canvasPlot(self):
        canvas = FigureCanvasTkAgg(f, self)
        self.animate()
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

    def animate(self):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + \
            self.ticket.get()+"&apikey=TU10HCWDTV5CNVBN"

        r = requests.get(url)
        data = r.json()

        dicto = []
        for valor in data["Time Series (Daily)"]:

            d = data["Time Series (Daily)"][valor]
            dicto.append(d)
        df = pd.DataFrame(dicto)
        value = df['4. close'].astype(float)
        a.clear()
        a.plot(value)
        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)
        a.set_title(self.ticket.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Series de Tiempo en Python")
    root.geometry("1200x600")
    TimeSeries(root).pack(side="top", fill="both", expand=True)

    # menubar todo feo
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(
        label="Open", command=lambda: popupmsg("Not supported just yet!"))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=quit)
    menubar.add_cascade(label="File", menu=filemenu)

    EditMenu = tk.Menu(menubar, tearoff=0)
    EditMenu.add_command(label="Copy")
    EditMenu.add_command(label="Other")
    menubar.add_cascade(label="Edit", menu=EditMenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index")
    helpmenu.add_command(label="About...")
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)
    # fin del menu
    root.mainloop()
