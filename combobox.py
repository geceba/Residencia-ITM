from tkinter import *
from tkinter import ttk
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Tkinter Combobox")
        self.minsize(640, 400)
        self.InitUi()

    def clickMe(self):
        self.label.configure(text = "You have selected "+ self.myfruit.get())    
    
    def InitUi(self):
        self.myfruit = StringVar()

        self.combo = ttk.Combobox(self, width= 15, textvariable= self.myfruit)
        self.combo['values'] = ("Apple", "Pear", "Melon", "Water Melon")
        self.combo.grid(column=1, row=0)

        self.label = ttk.Label(self, text = "Select your favorite fruit")
        self.label.grid(column = 0, row=0)

        self.button = ttk.Button(self, text="Click me", command = self.clickMe)
        self.button.grid(column = 1, row = 1)

if __name__ == 'main':
    root = Root()
    root.mainloop()