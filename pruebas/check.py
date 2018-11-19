from tkinter import *
def Ver():
   print([var.get() for var in states])
root = Tk()
states = []

for i in range(5,50,5):

   var = IntVar()

   chk = Checkbutton(root, text=str(i), variable=var, command=Ver)

   chk.pack(side=LEFT)

   states.append(var)


root.mainloop()