import sqlite3
from crud import CRUD as cr
import tkinter.ttk as ttk

con_bd = sqlite3.connect('bd.sqlite3')

cursor = con_bd.cursor()

# leer base de datos
"""
cursor.execute("SELECT * FROM tickets")

lista = []

for i in cursor:
    lista.append(i[0])
 """   


# pruebas para el combobox
name = input("Ingrese el nombre cort\n")
full_name = input("Ingrese el nombre completo\n")

cr.insert(con_bd, name, full_name)


"""
cbx = ttk.Combobox(values=lista, state='readonly')
cbx.current(0)
cbx.configure(width=25)

cbx.pack()
cbx.master.title("ttk widgets")
cbx.mainloop()
"""


