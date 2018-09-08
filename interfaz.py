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
    popup.wm_title("epppa")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

mensaje = ""
def message(cadena):
	toUpper = cadena.get()
	global mensaje
	mensaje += toUpper.upper()
	secret = prinM()
	#animate(secret)
def prinM():
	return mensaje
# la funcion animate permite leer y animar la data en una grafica
# este metodo permitira filtrar la informacion correcta
def animate():
	#print("mensaje "+ msg)
	mensaje="MSFT"
	url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+mensaje+"&apikey=TU10HCWDTV5CNVBN"
	print(url)
	r = requests.get(url)
	data = r.json()
	#print(type(data))
	
	dicto = []
	for valor in data["Time Series (Daily)"]:
		#print(data["Time Series (Daily)"][valor]["1. open"])
		d = data["Time Series (Daily)"][valor]
		dicto.append(d)
	df= pd.DataFrame(dicto)
	value = df['4. close'].astype(float)
	a.clear()
	a.plot(value)
	a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)
	a.set_title('Time Series')
	

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

		self.show_frame(Graph_Page) # show frame es lo primero que mostrará

	def show_frame(self, cont):
		# Obtiene el frame de la pagina que estamos llamando
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text=("""Bienvenido a la aplicacion de analisis de datos"""), font=LARGE_FONT)
		label.pack( pady=10, padx=10)

		ticket = tk.Label(self, text=("""Ticket"""), font=LARGE_FONT)
		ticket.pack(pady=2)

		inputicket = tk.StringVar()
		inputT = tk.Entry(self,  textvariable=inputicket)
		inputT.pack(pady=5)

		button1 = ttk.Button(self, text="Iniciar", command=lambda: [controller.show_frame(Graph_Page), message(inputicket)])
		button1.pack()


class Graph_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		label = tk.Label(self, text="Grafica", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		animate()
		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

app = SeaofBTCapp()
#ani = animation.FuncAnimation(f, animate, interval = 100000)
app.mainloop()