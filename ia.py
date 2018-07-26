from tkinter import *

def obtener():
    data = 'https://www.google.com/finance/getprices?i=600&p='+days.get()+'d&f=d,o,h,l,c,v&df=cpct&q='+emp_entry.get()
    print(data)



root = Tk()
root.geometry("900x400")
root.title("Series Data")


# primer frame para la parte de captura de datos
frame = Frame(root)
frame.grid(row=0, column=0, sticky="e", padx=5, pady=5)
frame.config(relief="ridge", bd=2)


ticker = Label(frame, text="Ticker")
ticker.grid(row=0, column=0, sticky="e",padx=5, pady=5)

#ingresar a que quieres evaluar
emp_entry = StringVar()
empresa = Entry(frame, textvariable=emp_entry)
empresa.grid(row=0, column=1, padx=5, pady=5)

plot = Button(frame, text="plot", command=obtener)
plot.grid(row=1, column=0)




#ingresar el numerode dias
lblDays = Label(frame, text="Days")
lblDays.grid(row=2, column=0)

days = StringVar()
entryDays = Entry(frame, textvariable=days)
entryDays.grid(row=2, column=1, padx=5, pady=5)


#segundo frame para la parte de los matplots




root.mainloop()