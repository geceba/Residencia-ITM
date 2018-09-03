# Bibliotecas
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import	style

import tkinter as tk
from tkinter import ttk

import requests
import csv
import pandas as pd, numpy as np, datetime

LARGE_FONT = ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
style.use("ggplot")

# figure permite dibujar, en este caso permite mostrar la grafica
# add_subplot agregar al canvas en este caso el figure
f = Figure(figsize=(10,5), dpi=100)
a = f.add_subplot(111)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# la funcion animate permite leer y animar la data en una grafica
# este metodo permitira filtrar la informacion correcta
def animate(i):
	r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=TU10HCWDTV5CNVBN")
	data = r.json()
	#print(type(data))
	
	dicto = []
	for valor in data["Time Series (Daily)"]:
		#print(data["Time Series (Daily)"][valor]["1. open"])
		d = data["Time Series (Daily)"][valor]
		dicto.append(d)
	df= pd.DataFrame(dicto)
	value = df['4. close'].astype(float)
	a.plot(value)
	

#esta clase es la principal, aqui llamo lo que necesito en la interfaz
# tk.Tk es el parametro que necesitamos para llamar la biblioteca que nos permite realizar la interfaz
class SeaofBTCapp(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.iconbitmap(self, default="icon.ico") # icono del programa
		tk.Tk.wm_title(self, "Analisis de Datos") # agregar titulo al programa

		container = tk.Frame(self) # contenedor del marco

		container.pack(side="top", fill="both", expand=True) # pack sirve para agregar lo que creamos al marco

		container.grid_rowconfigure(0, weight=1) # en esta modificamos filas y columnas, esta parte del codigo solo es el contenedor
		container.grid_columnconfigure(0, weight=1)

		menubar = tk.Menu(container)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=quit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		tk.Tk.config(self, menu=menubar)

		self.frames = {} # diccionario vacio para agregar al frame padre

		# recorremos las dos clases StartPage y BTC, son nada mas nuevas ventanas
		for F in (StartPage, Graph_Page):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage) # show frame es lo primero que mostrara

	def show_frame(self, cont):
		# Obtiene el frame de la pagina que estamos llamando
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text=("""Bienvenido a la aplicacion de analisis de datos"""), font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Iniciar", command=lambda: controller.show_frame(Graph_Page))
		button1.pack()

		#button2 = ttk.Button(self, text="Salir", command=quit)
		#button2.pack()

class Graph_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Grafica", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Regresar a la página principal", command=lambda: controller.show_frame(StartPage))
		button1.pack()

		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval = 100000)
app.mainloop()