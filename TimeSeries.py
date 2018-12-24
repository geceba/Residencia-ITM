import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

import sqlite3
from crud import CRUD as cr
from arima import ModeloArima as ar
from popup import PopUp as pop

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
style.use("ggplot")

f = Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(111) # linea de datos normales
b = f.add_subplot(111) # linea de los datos con la media movil
c = f.add_subplot(111) # linea de los datos del forecast
upper = f.add_subplot(111)
lower = f.add_subplot(111)

con_bd = sqlite3.connect('bd.sqlite3')

# crear la conexion con la base de datos


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("epppa")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10, padx=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

class TimeSeries(tk.Frame):

    # Inicializar la interfaz desde el constructor
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        label = tk.Label(self, text=(
            """Bienvenido a la aplicación de análisis de datos"""))
        label.grid(row=0, column=0)
        self.InitUi()
        self.canvasPlot()

    # Definir los valores o elementos que tendra la interfaz
    def InitUi(self):
        self.label = ttk.Label(self, text="Seleccione su ticker")
        self.label.grid(row=1, column=0)

        self.ticket = tk.StringVar()
        lista_nombres = cr.select(con_bd)

        self.combo = ttk.Combobox(
        self, width=15, textvariable=self.ticket, state='readonly', values=lista_nombres)
        

        self.combo.current(1)
        self.combo.grid(row=2, column=0)

        self.combo.bind("<<ComboboxSelected>>")
    
        self.content_frame()

    # limpiar las lineas cuando se cambie de ticket
    def clickMe(self):
        a.clear()
        self.canvasPlot()
        
    # canvasPlot es el que realiza el despliegue de las lineas
    def canvasPlot(self):
        

        canvas = FigureCanvasTkAgg(f, self)
        
        self.grafica()

        canvas.draw()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=5, column=0)

     

    # contenido del frame para agregarlo al principal
    def content_frame(self):
        master = tk.Frame(self)
        fecha_1 = tk.Label(master, text='Fecha Inicio').grid(row=0,column=1)
        
        
        global entry_end, entry_start, start, end

        entry_start = tk.StringVar()
        entry_end = tk.StringVar()

        start = tk.IntVar()
        end = tk.IntVar()

        fecha_entry_1 = tk.Entry(master, textvariable=entry_start).grid(row=0, column=2)


        fecha_2 = tk.Label(master, text='Fecha Fin').grid(row=0, column=3)

        fecha_entry_2 = tk.Entry(master, textvariable=entry_end).grid(row=0, column=4)
        
        lbl_start = tk.Label(master, text='Punto Inicio').grid(row=1, column=1)
        p_start = tk.Entry(master, textvariable=start).grid(row=1, column=2)

        lbl_end = tk.Label(master, text="Punto Fin").grid(row=1, column=3)
        p_end = tk.Entry(master, textvariable=end).grid(row=1, column=4)

        botonTest = tk.Button(master, text='Graficar', command= self.clickMe, padx=20, pady=5).grid(row=2, column=2)
        
        exportar = tk.Button(master, text="Close csv", command=self.csv_export, padx=20, pady=5).grid(row=2, column=3)
        master.grid(row=3, column=0)

        exportar_forecast = tk.Button(master, text="Predicción", padx=20, pady=5).grid(row=2, column=4)

    # forma rápida para obtener el valor del dataframe y mandarlo a un formato csv
    def csv_export(self):
        export_csv = value.to_csv(r''+self.ticket.get()+time.strftime("%c")+'.csv',  index = True, header=True)
    
    
    def grafica(self):
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
        # renombrar las columnas  
        df = df.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df.sort_index(inplace=True)
        # extraer la informacion que quiero
        global value
        value = df['Close'].astype(float)


        #print("valor: " ,entry_start.get())
        #print("numero: ", type(start.get()))

        
        modelo_arima = ar.arima_modelo(value, entry_start.get(), entry_end.get())
        ari = ar.tendencia(modelo_arima, start.get(), end.get())

        reporte = modelo_arima.summary()
        html = reporte.as_html()


        with open('result.html', 'w+') as myfile:
            myfile.write("<html><head><link <link rel='stylesheet' href='estilos.css'></head><body>")
            myfile.write(html)
            myfile.write("</body></html>")

        df['forecast'] = ari
        resultados = df['forecast']


        df.dropna(inplace=True)

        df.index = pd.to_datetime(df.index)


        # calcular la media movil en un nuevo df, da un error de logico y no muesta todos los datos cuando se trata de sobreesribir
        
        data_frame = pd.DataFrame(value)
        data_frame['MA'] = data_frame['Close'].rolling(window=12).mean()
        data_frame['STD'] = data_frame['Close'].rolling(window=12).std()
        data_frame['Upper Band'] = data_frame['MA'] + (data_frame['STD'] * 2)
        data_frame['Lower Band'] = data_frame['MA'] - (data_frame['STD'] * 2)

       # MovingAvarage = value.rolling(window=6).mean()
        
        #newdata = newdata.rename(columns={"datetime": "datetime", "Close": "Media Movil"})
        #newdata = pd.DataFrame(MovingAvarage)
        #df['Upper Band'] = df['MA'] + (df['STD'] * 2)
        #df['STD'] = df['Close'].rolling(window=12).std()
        #df['Lower Band'] = df['MA'] - (df['STD'] * 2)
     
        a.clear()
        b.clear()
        c.clear()
        upper.clear()
        lower.clear()

        a.set_xlabel("Fecha")
        a.set_ylabel("Valores de Cierre")        

        a.plot(value, color='b')
        b.plot(data_frame['MA'], color='m')
        c.plot(resultados, color='y')
        upper.plot(data_frame['Upper Band'], color='g')
        lower.plot(data_frame['Lower Band'], color='r')
        lower.legend(loc="upper right")
        

# __name__  es donde creo la raiz de la interfaz

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Series de Tiempo en Python")
    root.geometry("1000x700")
    TimeSeries(root).pack(side="top", fill="both", expand=True)
    #root.iconbitmap(default="icon.ico")
    # menubar todo feo
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(
        label="Open", command=lambda: popupmsg("Not supported just yet!"))
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=quit)
    menubar.add_cascade(label="Archivo", menu=filemenu)

    EditMenu = tk.Menu(menubar, tearoff=0)
    EditMenu.add_command(label="Insertar ticker", command=lambda:pop.insert_data(con_bd))
    EditMenu.add_command(label="Borrar ticker", command=lambda:pop.delete_data(con_bd))
    menubar.add_cascade(label="Edit", menu=EditMenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Mostrar Descripción", command=pop.openHtml)
    helpmenu.add_command(label="Acerca de...")
    menubar.add_cascade(label="Ayuda", menu=helpmenu)

    root.config(menu=menubar)
    root.configure(background='white')
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    # fin del menu
    root.mainloop()
