import tkinter as tk
from tkinter import ttk
from crud import CRUD as cr


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)


class PopUp:
    def insert_data(con):
        
        def show_entry_fields():
            #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
            cr.insert(con, e1.get(), e2.get())

        master = tk.Tk()
        master.wm_title("Insertar Datos")
        tk.Label(master, text="Ticket: ").grid(row=0)
        tk.Label(master, text="Empresa: ").grid(row=1)

        e1 = tk. Entry(master)
        e2 = tk. Entry(master)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Salir', command=master.destroy).grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Button(master, text='Agregar', command=show_entry_fields).grid(row=3, column=1, sticky=tk.W, pady=5)

        master.mainloop( )