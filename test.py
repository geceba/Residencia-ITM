from tkinter import *
import sqlite3
from crud import CRUD as cr


class ListBoxTest :
    def __init__(self) :
        con_bd = sqlite3.connect('bd.sqlite3')
        self.root = Tk()
        self.list_box_1 = Listbox(self.root, selectmode=EXTENDED)
        self.list_box_1.pack()
        self.delete_button = Button(self.root, text="Delete",command=self.DeleteSelection)
        self.delete_button.pack()

        for i in cr.select(con_bd) :
            s = i
            self.list_box_1.insert( END,s )
        self.root.mainloop()

    def DeleteSelection(self):
        items = self.list_box_1.curselection()
        
        
        pos = 0
        print(items)
        for i in items :
            idx = int(i) - pos
            hola = self.list_box_1.get(i, END)
            self.valor(hola[0])
            self.list_box_1.delete( idx,idx )
            pos = pos + 1

    def valor(self,name):
        con_bda = sqlite3.connect('bd.sqlite3')
        cr.delete(con_bda, name)

lbt=ListBoxTest()


