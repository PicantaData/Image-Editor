from email.mime import image
from logging import root
from tkinter import *
from PIL import ImageTk,Image,ImageChops,ImageFilter
from tkinter import filedialog
from tkinter import colorchooser
import numpy as np

root = Tk()
root.title('Image Editor')
width_window= root.winfo_screenwidth()               
height_window= int(0.92*root.winfo_screenheight())               
root.geometry(f"{width_window}x{height_window}")
root.state('zoomed')

#Converting jpg image to .ico and placing it on title window
to_convert = Image.open('image-editing-icon.jpg')
converted_pic = ImageTk.PhotoImage(to_convert)
root.wm_iconphoto(False, converted_pic)

#LEFT-FRAME
f_left_width = 0.75*width_window
f_left_height = height_window
frame_left = LabelFrame(root,bg="lightgreen",text="Workspace",labelanchor=NW,padx=10,pady=10,width=f_left_width,height=f_left_height)
frame_left.grid(row=0,column=0)
frame_left.grid_propagate(0)

#LEFT-FRAME_CANVAS
global canvas_width
global canvas_height
canvas_width = int(0.95*f_left_width)
canvas_height = int(0.9*f_left_height)
img_canvas = Canvas(frame_left,width=canvas_width,height=canvas_height, bg="white")
img_canvas.grid(row=0,column=0,pady=5)
#img_canvas.place(relx=0.5,anchor=N)
img_canvas.grid_propagate(0)

#CANVAS_COLOUR_CHOOSING-BUTTON
def canvas_bg_color():
    choose_colour = colorchooser.askcolor()[1]
    img_canvas["bg"] = f"{choose_colour}"

change_col_canvas = Button(frame_left,text="Change Canvas' Colour",font=("Arial","10", "bold","italic"),border=2,justify=CENTER,cursor="hand2",command=canvas_bg_color,padx=5)
#change_col_canvas.place(relx=0.5,rely=1,anchor=S)
change_col_canvas.grid(row=1,columnspan=2)

#RIGHT-FRAME
f_right_width = 0.25*width_window
f_right_height = height_window
frame_right = LabelFrame(root,text="TOOLS",labelanchor=N,bg="lightblue",padx=5,pady=5,width=f_right_width,height=f_right_height)
frame_right.grid(row=0,column=1)
frame_right.grid_propagate(0)

#RIGHT-FRAME-TOOLS

#IMPORT-BUTTON
def import_img():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    frame_left.imgaddress = filedialog.askopenfilename(initialdir="/",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    pillow_image = Image.open(frame_left.imgaddress)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)

    #Label mehod
    #open_image = ImageTk.PhotoImage(Image.open(frame_left.imgaddress))
    #open_image_label = Label(img_canvas,image= open_image_canvas)
    #open_image_label.grid(row=0,column=0,padx=10,pady=10)
      
insert_img_button = Button(frame_right, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
insert_img_button.grid(row=0,column=0,columnspan=2,padx=0.35*f_right_width,pady=20)
#insert_img_button.place(relx=0.5,anchor=N,y=20)

#EDITING-BUTTONS
def rotate_right90():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.rotate(270)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)

rotate_right = Button(frame_right,text="Rotate Right",bg="black",command=rotate_right90,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
rotate_right.grid(row=1,column=1,padx=10,pady=10)
#rotate_right.place(relx=0.8,y=80,anchor=E)

def rotate_left90():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.rotate(90)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)

rotate_left = Button(frame_right,text="Rotate Left",bg="black",command=rotate_left90,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
rotate_left.grid(row=1,column=0,padx=10,pady=10)
#rotate_left.place(relx=0.2,y=80,anchor=W)

def flip_left_right():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.transpose(Image.FLIP_LEFT_RIGHT)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)

flip_lr_button = Button(frame_right,text="Flip Left-Right",bg="black",command=flip_left_right,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
flip_lr_button.grid(row=2,column=0,padx=10,pady=10)
#rotate_left.place(relx=0.2,y=120,anchor=W)

def flip_top_bottom():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.transpose(Image.FLIP_TOP_BOTTOM)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)


flip_tb_button = Button(frame_right,text="Flip Top-Bottom",bg="black",command=flip_top_bottom,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
flip_tb_button.grid(row=2,column=1,padx=10,pady=10)
#rotate_right.place(relx=0.8,y=120,anchor=E)

def greyscale():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.convert('L')
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)
   
button_greyscale = Button(frame_right,text="Convert to Black & White",bg="black",command=greyscale,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_greyscale.grid(row=3,columnspan=2,padx=10,pady=10)
#button_greyscale.place(relx=0.5,y=160,anchor=E)


#Entry Boxes
cropping_parametersx1 = Entry(frame_right)
cropping_parametersx1.grid(row=4,column=0,padx=10,pady=10)
cropping_parametersx1.insert(0,"x coord. top-left")

cropping_parametersy1 = Entry(frame_right)
cropping_parametersy1.grid(row=4,column=1,padx=10,pady=10)
cropping_parametersy1.insert(0,"y coord. top-left")

cropping_parametersx2 = Entry(frame_right)
cropping_parametersx2.grid(row=5,column=0,padx=10,pady=10)
cropping_parametersx2.insert(0,"x coord. bottom-right")

cropping_parametersy2 = Entry(frame_right)
cropping_parametersy2.grid(row=5,column=1,padx=10,pady=10)
cropping_parametersy2.insert(0,"y coord. bottom-right")

def crop():
    global pillow_image
    global pillow_image_arr
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image_arr = np.array(pillow_image)
    pillow_image_arr = pillow_image_arr[int(cropping_parametersy1.get()):int(cropping_parametersy2.get()),int(cropping_parametersx1.get()):int(cropping_parametersx2.get())]
    pillow_image = Image.fromarray(pillow_image_arr)
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)
    
    cropping_parametersx1.delete(0,END)
    cropping_parametersy1.delete(0,END)
    cropping_parametersx2.delete(0,END)
    cropping_parametersy2.delete(0,END)
   
button_crop = Button(frame_right,text="Crop",bg="black",command=crop,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_crop.grid(row=6,columnspan=2,padx=10,pady=10)

def invert():
    global pillow_image
    global pillow_image_arr
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image_arr = np.array(pillow_image)
    colours_arr = pillow_image_arr[:,:,:3]
    inv_colours_arr = 255 - colours_arr

    is_png = pillow_image_arr.shape[2]==4
    if(is_png):
        alpha_ch = pillow_image_arr[:,:,3]
        inv_arr = np.dstack((inv_colours_arr,alpha_ch))
    else:
        inv_arr = inv_colours_arr
    
    pillow_image = Image.fromarray(inv_arr)
    
    image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=image_tk)
   
button_invert = Button(frame_right,text="Invert Colours",bg="black",command=invert,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_invert.grid(row=7,columnspan=2,padx=10,pady=10)

root.mainloop()