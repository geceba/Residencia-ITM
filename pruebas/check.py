import tkinter as tk
root=tk.Tk()

c1=tk.BooleanVar()
c2=tk.BooleanVar()
c3=tk.BooleanVar()
c4=tk.BooleanVar()

def get_value():
    for c in (c1,c2,c3,c4):
        print(c.get())

tk.Checkbutton(root,text='checkbox1',variable=c1,).pack()
tk.Checkbutton(root,text='checkbox2',variable=c2,).pack()
tk.Checkbutton(root,text='checkbox3',variable=c3,).pack()
tk.Checkbutton(root,text='checkbox4',variable=c4,).pack()
tk.Button(root,text='get value',command=get_value).pack()

root.mainloop()