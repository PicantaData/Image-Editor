from logging import root
from tkinter import *

root = Tk()

def onClick():
    my_label = Label(root, text="Hello User!")
    my_label.grid(row="5",column="5")

my_button = Button(root,text="Say Hello!",command = onClick)
my_button.grid(row="0",column="5")

root.mainloop()