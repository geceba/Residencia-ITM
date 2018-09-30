import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import requests
import pandas as pd
import numpy as np

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
style.use("ggplot")

f = Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(111)
b = f.add_subplot(111)
c = f.add_subplot(111)


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
        self.canvasPlot()

    def InitUi(self):
        self.label = ttk.Label(self, text="Seleccione su ticket")
        self.label.grid(row=1, column=0)

        self.ticket = tk.StringVar()
        self.combo = ttk.Combobox(
            self, width=15, textvariable=self.ticket, state='readonly')
        self.combo['values'] = ("AAPL", "MSFT", "AMZN", "GOOG", "ORCL")
        self.combo.current(2)
        self.combo.grid(row=2, column=0)

        self.combo.bind("<<ComboboxSelected>>", self.clickMe)

        self.button = ttk.Button(self, text="Click me")
        self.button.grid(row=3, column=0)

    def clickMe(self, event):
        a.clear()
        self.canvasPlot()

    def canvasPlot(self):
        canvas = FigureCanvasTkAgg(f, self)
        self.animate()
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

    def animate(self):
        url ="https://www.alphavantage.co/query"

        params = {
            "function":"TIME_SERIES_DAILY_ADJUSTED",
            "symbol": self.ticket.get(),
            "apikey": "TU10HCWDTV5CNVBN"
        }

        response = requests.get(url, params=params)
        data = response.json()

        def convert_response(d):
            for dt, prec in d['Time Series (Daily)'].items():
                r = {'datetime': dt}
                r.update(prec)
                yield r

        df = pd.DataFrame(convert_response(data))
        # rename the columns    
        df = df.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df.sort_index(inplace=True)
        # extract the columns you want
        value = df['Close'].astype(float)
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index)
        df['6-SMA']=df['Close'].astype(float).rolling(window=6).mean()
        df['12-SMA']=df['Close'].astype(float).rolling(window=12).mean()
    
        
        a.clear()
        a.plot(value)


        #a.set_title(self.ticket.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Series de Tiempo en Python")
    root.geometry("1000x600")
    TimeSeries(root).pack(side="top", fill="both", expand=True)
    #root.iconbitmap(default="icon.ico")
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
