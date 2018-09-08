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
import csv
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
        label.pack(side=tk.TOP, expand=True)
        self.parent = parent

        self.InitUi()
        self.canvasPlot()

    def InitUi(self):

        self.label = ttk.Label(self, text="Seleccione su ticket")
        self.label.pack(side=tk.TOP)

        self.ticket = tk.StringVar()
        self.combo = ttk.Combobox(
            self, width=15, textvariable=self.ticket, state='readonly')
        self.combo['values'] = ("AAPL", "MSFT", "AMZN", "GOOG", "ORCL")
        self.combo.current(0)
        self.combo.pack()

        self.button = ttk.Button(self, text="Click me", command=self.animate)
        self.button.pack()

    def clickMe(self):
        print(self.ticket.get())

    def canvasPlot(self):
        canvas = FigureCanvasTkAgg(f, self)
        self.animate()
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def animate(self):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + \
            self.ticket.get()+"&apikey=TU10HCWDTV5CNVBN"
        print(url)
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
    root.geometry("900x400")
    TimeSeries(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
