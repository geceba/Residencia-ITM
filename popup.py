import tkinter as tk
from tkinter import ttk
from crud import CRUD as cr
import webbrowser
import pandas as pd

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)


class PopUp:
    def insert_data(con):
        
        def show_entry_fields():
            #print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
            if len(e1.get()) > 0  and len(e2.get()) > 0:
                cr.insert(con, e1.get(), e2.get())
                master.destroy()
            elif len(e1.get()) == 0:
                e1.config(highlightbackground="red")
                e1.focus()
            elif len(e2.get()) == 0:
                e2.focus()

        master = tk.Tk()
        master.geometry("400x300")
        master.wm_title("Insertar Datos")
        tk.Label(master, text="Ticker: ").grid(row=0, ipady=10)
        tk.Label(master, text="Empresa: ").grid(row=1, ipady=10)

        e1 = tk.Entry(master)
        e2 = tk.Entry(master)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Salir', command=master.destroy).grid(row=3, column=0, sticky=tk.W, ipady=10, ipadx=40, padx=30, pady=40)
        tk.Button(master, text='Agregar', command=show_entry_fields).grid(row=3, column=1, sticky=tk.W, ipady=10, ipadx=60, pady=40)

        master.mainloop( )
    
    def delete_data(con):

        conexion = con        

        def DeleteSelection():
            items = list_box_1.curselection()
        
        
            pos = 0
            #print(items)
            for i in items :
                idx = int(i) - pos
                data = list_box_1.get(i, tk.END)
                cr.delete(conexion, data[0])
                list_box_1.delete( idx,idx )
                pos = pos + 1

        root = tk.Tk()
        root.geometry("300x250")
        root.wm_title("Eliminar Datos")
        list_box_1 = tk.Listbox(root, selectmode=tk.EXTENDED)
        list_box_1.pack()
        delete_button = tk.Button(root, text="Eliminar",command=DeleteSelection)
        delete_button.pack()

        for i in cr.select(con) :
            s = i
            list_box_1.insert( tk.END, s)
        root.mainloop()

    def openHtml():
        webbrowser.open('file:///Users/gcetzal/python-projects/Residencia-ITM/result.html', new=2)
    

