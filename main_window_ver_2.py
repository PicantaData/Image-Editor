from logging import root
from tkinter import *
from PIL import ImageTk,Image,ImageChops,ImageFilter
from tkinter import filedialog
from tkinter import colorchooser
import numpy as np
from matplotlib import pyplot as plt

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
canvas_width = 0.95*f_left_width
canvas_height = 0.9*f_left_height
img_canvas = Canvas(frame_left,width=canvas_width,height=canvas_height, bg="white", highlightbackground="gray",cursor="plus")
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
def resize(original_img):
    global canvas_height,canvas_width
    
    aspect_ratio = pillow_image.size[1]/pillow_image.size[0]
    new_width = canvas_height/aspect_ratio
    new_height = canvas_width*aspect_ratio
    if(original_img.size[1] >= canvas_height and original_img.size[0] > canvas_width):
        if(new_width >= canvas_width):
            resized_img=ImageTk.PhotoImage(original_img.resize((int(canvas_width),int(new_height))))
            return resized_img
        else:
            resized_img=ImageTk.PhotoImage(original_img.resize((int(new_width),int(canvas_height))))
            return resized_img
    elif(original_img.size[1] >= canvas_height):
        resized_img=ImageTk.PhotoImage(original_img.resize((int(new_width),int(canvas_height))))
        return resized_img
    elif(original_img.size[0] >= canvas_width):
        resized_img=ImageTk.PhotoImage(original_img.resize((int(canvas_width),int(new_height))))
        return resized_img
    else:
        resized_img = ImageTk.PhotoImage(original_img)
        return resized_img

#IMPORT-BUTTON
def import_img():
    global pillow_image,image_tk,resized_image_tk,image_on_canvas,canvas_width,canvas_height,aspect_ratio
    
    frame_left.imgaddress = filedialog.askopenfilename(initialdir="/",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    
    pillow_image = Image.open(frame_left.imgaddress)
    
    image_tk = ImageTk.PhotoImage(pillow_image)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    #image_tk = ImageTk.PhotoImage(pillow_image)
    '''
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''

insert_img_button = Button(frame_right, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
insert_img_button.grid(row=0,column=0,columnspan=2,padx=0.35*f_right_width,pady=20)


#EDITING-BUTTONS
def rotate(var):
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    global pillow_image_copy
    
    pillow_image_copy = pillow_image.copy()
    pillow_image_copy = pillow_image_copy.rotate(rotate_.get(),expand=True,resample=Image.NEAREST)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image_copy)
    
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image_copy.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
rotate_ = Scale(frame_right,from_=-180,to=180,orient=HORIZONTAL,command=rotate)
rotate_.grid(row=1,column=0,padx=10,pady=10)

def rotate_final():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    global pillow_image_copy
    
    pillow_image = pillow_image_copy
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
rotate_final_button = Button(frame_right,text="Update_rotated",bg="black",command=rotate_final,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
rotate_final_button.grid(row=1,column=1,padx=10,pady=10)
##
'''def rotate_right90():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.rotate(270)
    image_tk = ImageTk.PhotoImage(pillow_image)
    
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)

rotate_right = Button(frame_right,text="Rotate Right",bg="black",command=rotate_right90,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
rotate_right.grid(row=1,column=1,padx=10,pady=10)

def rotate_left90():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height

    pillow_image = pillow_image.rotate(90)
    image_tk = ImageTk.PhotoImage(pillow_image)
    
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)

rotate_left = Button(frame_right,text="Rotate Left",bg="black",command=rotate_left90,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,)
rotate_left.grid(row=1,column=0,padx=8,pady=10)
'''
def flip_left_right():
    global pillow_image
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height

    pillow_image = pillow_image.transpose(Image.FLIP_LEFT_RIGHT)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
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
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''

flip_tb_button = Button(frame_right,text="Flip Top-Bottom",bg="black",command=flip_top_bottom,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
flip_tb_button.grid(row=2,column=1,padx=10,pady=10)
#rotate_right.place(relx=0.8,y=120,anchor=E)

def greyscale():
    global pillow_image
    global pillow_image_arr
    global image_tk
    global resized_image_tk
    global image_on_canvas
    global canvas_width
    global canvas_height
    
    pillow_image = pillow_image.convert('L')
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
button_greyscale = Button(frame_right,text="Grey Scale",bg="black",command=greyscale,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_greyscale.grid(row=3,columnspan=2,padx=10,pady=10)

'''
show_grid_button = Button(frame_right,text="Show Grid",bg="black",command=show_grid,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
show_grid_button.grid(row=6,column=0,padx=10,pady=10)  '''

def open_plot():
    global pillow_image
    plt.subplot(111)
    plt.imshow(pillow_image)
    plt.show()

button_show_grid = Button(frame_right,text="See Reference Scale",bg="black",command=open_plot,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_show_grid.grid(row=6,column=0,padx=10,pady=10)
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
    plt.close()
    #Using slicing method
    pillow_image_arr = np.array(pillow_image)
    pillow_image_arr = pillow_image_arr[int(cropping_parametersy1.get()):int(cropping_parametersy2.get()),int(cropping_parametersx1.get()):int(cropping_parametersx2.get())]
    pillow_image = Image.fromarray(pillow_image_arr)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
    cropping_parametersx1.delete(0,END)
    cropping_parametersy1.delete(0,END)
    cropping_parametersx2.delete(0,END)
    cropping_parametersy2.delete(0,END)

button_crop = Button(frame_right,text="Crop",bg="black",command=crop,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_crop.grid(row=6,column=1,padx=10,pady=10)

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
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    '''image_tk = ImageTk.PhotoImage(pillow_image)
    #size_image = list(image_tk.size())
    if (image_tk.width!= canvas_width or image_tk.height!=canvas_height):
        resized_image_tk = ImageTk.PhotoImage(pillow_image.resize((canvas_width,canvas_height)))
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=resized_image_tk)
    else:
        image_on_canvas = img_canvas.create_image(canvas_width/2,0,anchor=N,image=image_tk)
    '''
button_invert = Button(frame_right,text="Invert Colours",bg="black",command=invert,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_invert.grid(row=7,columnspan=2,padx=10,pady=10)

def save_file():
    global pillow_image
    file_name = filedialog.asksaveasfile(mode='w', defaultextension=".jpeg", filetypes=[("JPG File",".jpg"),("PNG File",".png"),("JPEG File",".jpeg")])
    if not file_name:
        return
    pillow_image.save(file_name)

button_save = Button(frame_right,text="Save this image",bg="black",command=save_file,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
button_save.grid(row=8,columnspan=2,padx=10,pady=10)

root.mainloop()