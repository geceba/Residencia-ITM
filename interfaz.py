import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import	style


import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd, numpy as np, datetime

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

# figure permite dibujar, en este caso permite mostrar la grafica
# add_subplot agregar al canvas en este caso el figure
f = Figure(figsize=(6,4), dpi=100)
a = f.add_subplot(111)


# la funcion animate permite leer y animar la data en una grafica
# este metodo permitira filtrar la informacion correcta
def animate(i):
    x = np.array(pd.read_csv("http://www.google.com/finance/getprices?q=AAPL&i=300&p=10d&f=d,o,h,l,c,v", skiprows=7, header=None))
    date=[]
    for i in range(0, len(x)):
        if x[i][0][0]=='a':
            t= datetime.datetime.fromtimestamp(int(x[i][0].replace('a','')))
            date.append(t)
        else:
            date.append(t+datetime.timedelta(minutes =int(x[i][0])))
    data1=pd.DataFrame(x, index=date)
    data1.columns=['a', 'Open', 'High','Low','Close','Vol']
	
	# limpiamos a para poder agregar y el plot agregara la data que se lee
    a.clear()
    a.plot(data1['Close'])

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

		self.frames = {} # diccionario vacio para agregar al frame padre

		# recorremos las dos clases StartPage y BTC, son nada mas nuevas ventanas
		for F in (StartPage, BTCe_Page):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage) # show frame es lo primero que mostrara

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text=("""Bienvenido a la aplicacion de analisis de datos"""), font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Iniciar", command=lambda: controller.show_frame(BTCe_Page))
		button1.pack()

		button2 = ttk.Button(self, text="Salir", command=quit)
		button2.pack()

class BTCe_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Grafica", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Regresar a la página principal", command=lambda: controller.show_frame(StartPage))
		button1.pack()

		

		canvas = FigureCanvasTkAgg(f, self)
		canvas.show()
		canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

		toolbar = NavigationToolbar2TkAgg(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()