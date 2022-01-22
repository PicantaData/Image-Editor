from email.mime import image
from logging import root
import textwrap
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import colorchooser

root = Tk()
root.title('Image Editor')
width_window= root.winfo_screenwidth()               
height_window= root.winfo_screenheight()               
root.geometry(f"{width_window}x{height_window}")

#Converting jpg image to .ico and placing it on title window
to_convert = Image.open('image-editing-icon.jpg')
converted_pic = ImageTk.PhotoImage(to_convert)
root.wm_iconphoto(False, converted_pic)

#LEFT-FRAME
f_left_width = 0.75*width_window
f_left_height = 0.916*height_window
frame_left = LabelFrame(root,bg="lightgreen",text="Workspace",labelanchor=NW,padx=10,pady=10,width=f_left_width,height=f_left_height)
frame_left.grid(row=0,column=0)
frame_left.grid_propagate(0)

#LEFT-FRAME_CANVAS
img_canvas = Canvas(frame_left,width=(0.95*f_left_width),height=(0.9*f_left_height), bg="white")
img_canvas.place(relx=0.5,anchor=N)
img_canvas.grid_propagate(0)

#RIGHT-FRAME
f_right_width = 0.25*width_window
f_right_height = 0.916*height_window
frame_right = LabelFrame(root,text="TOOLS",labelanchor=N,bg="lightblue",padx=5,pady=5,width=f_right_width,height=f_right_height)
frame_right.grid(row=0,column=1)
frame_right.grid_propagate(0)

#CANVAS_COLOUR_CHOOSING-BUTTON
def canvas_bg_color():
    choose_colour = colorchooser.askcolor()[1]
    img_canvas["bg"] = f"{choose_colour}"

change_col_canvas = Button(frame_left,text="Change Canvas' Colour",font=("Arial","10", "bold","italic"),command=canvas_bg_color,padx=5)
change_col_canvas.place(relx=0.5,rely=1,anchor=S)

#IMPORT-BUTTON
def import_img():
    global open_image
    frame_left.imgaddress = filedialog.askopenfilename(initialdir="/",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    open_image = ImageTk.PhotoImage(Image.open(frame_left.imgaddress))
    open_image_label = Label(img_canvas,image=open_image)
    open_image_label.grid(row=0,column=0,padx=10,pady=10)
      
insert_img_button = Button(frame_right, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
#insert_img_button.grid(row=0,column=0,padx=0.35*f_right_width,pady=20)
insert_img_button.place(relx=0.5,anchor=N,y=20)

root.mainloop()