from logging import root
from tkinter import *
from PIL import ImageTk,Image,ImageChops,ImageFilter,ImageEnhance
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

#IMAGE-ADJUSTMENT
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

#ENABLE TOOLS
def enable():
    sharpen_["state"] = NORMAL
    contrast_["state"] = NORMAL
    bright_["state"] = NORMAL
    rotate_["state"] = NORMAL
    sat_["state"] = NORMAL
    rotate_final_button["state"] = NORMAL
    flip_lr_button["state"] = NORMAL
    flip_tb_button["state"] = NORMAL
    button_greyscale["state"] = NORMAL
    button_invert["state"] = NORMAL
    button_crop["state"] = NORMAL
    apply_change_button["state"] = NORMAL
    button_save["state"] = NORMAL
    rotate_.set(0)
    bright_.set(10)
    contrast_.set(8)
    sharpen_.set(4)
    sat_.set(10)
    

#IMPORT-BUTTON
def import_img():
    global pillow_image,pillow_image_copy,resized_image_tk,image_on_canvas,canvas_width,canvas_height
    
    frame_left.imgaddress = filedialog.askopenfilename(initialdir="/",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    
    pillow_image = Image.open(frame_left.imgaddress)
    pillow_image_copy = pillow_image.copy()
    #image_tk = ImageTk.PhotoImage(pillow_image)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    enable()

insert_img_button = Button(frame_right, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED)
insert_img_button.grid(row=0,column=0,columnspan=2,padx=0.35*f_right_width,pady=20)


#EDITING-BUTTONS
#ROTATE
def rotate(var):
    global pillow_image,pillow_image_copy,pillow_image_copy1
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy1 = pillow_image_copy.copy()
    pillow_image_copy1 = pillow_image_copy1.rotate(-rotate_.get(),expand=True,resample=Image.NEAREST)
    resized_image_tk = resize(pillow_image_copy1)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)

rotate_ = Scale(frame_right,from_=-180,to=180,orient=HORIZONTAL,command=rotate,label="Rotate",state='disabled')
rotate_.grid(row=1,column=0,padx=10,pady=10)

def rotate_final():
    global pillow_image,pillow_image_copy,pillow_image_copy1
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image_copy1
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    rotate_.set(0)
   
rotate_final_button = Button(frame_right,text="Update Rotated Image",bg="black",command=rotate_final,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
rotate_final_button.grid(row=1,column=1,padx=10,pady=10)

#FLIP
def flip_left_right():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height

    pillow_image_copy = pillow_image_copy.transpose(Image.FLIP_LEFT_RIGHT)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
flip_lr_button = Button(frame_right,text="Flip Left-Right",bg="black",command=flip_left_right,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
flip_lr_button.grid(row=2,column=0,padx=10,pady=10)

def flip_top_bottom():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
     
    pillow_image_copy = pillow_image_copy.transpose(Image.FLIP_TOP_BOTTOM)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
flip_tb_button = Button(frame_right,text="Flip Top-Bottom",bg="black",command=flip_top_bottom,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
flip_tb_button.grid(row=2,column=1,padx=10,pady=10)

#IMAGE-COLOUR
def greyscale():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image_copy.convert('L')
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
button_greyscale = Button(frame_right,text="Grey Scale",bg="black",command=greyscale,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
button_greyscale.grid(row=9,column=0,padx=10,pady=10)

def sharpness(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk, image_on_canvas
    global canvas_width,canvas_height
    
    img_sharp = ImageEnhance.Sharpness(pillow_image_copy)
    pillow_image_copy = img_sharp.enhance(sharpen_.get()/4.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
sharpen_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=sharpness,label="Sharpness",state='disabled')
#sharpen_.set(4)
sharpen_.grid(row=3,column=1,padx=3,pady=10)

def contrast(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    img_cont = ImageEnhance.Contrast(pillow_image_copy)
    pillow_image_copy = img_cont.enhance(contrast_.get()/8.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
contrast_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=contrast,label= "Contrast",state='disabled')
#contrast_.set(8)
contrast_.grid(row=4,column=0,padx=3,pady=10)

def brightness(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    img_bright = ImageEnhance.Brightness(pillow_image_copy)
    pillow_image_copy = img_bright.enhance(bright_.get()/10.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
bright_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=brightness,label= "Brightness",state='disabled')

bright_.grid(row=4,column=1,padx=3,pady=10)

def saturation(var):
    global pillow_image,pillow_image_copy
    global image_tk,resized_image_tk
    global image_on_canvas
    global canvas_width,canvas_height
    
    img_sat = ImageEnhance.Color(pillow_image_copy)
    pillow_image_copy = img_sat.enhance(sat_.get()/10.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
sat_ = Scale(frame_right,from_=0,to=30,orient=HORIZONTAL,command=saturation,label= "Saturation",state='disabled')
#sat_.set(10)
sat_.grid(row=3,column=0,padx=10,pady=10)

#CROP_AREA_RECTANGLE
def select_area():
    global rect
    
    def on_press(event):
        global Start_X,Start_Y,rect,image_on_canvas
        Start_X = img_canvas.canvasx(event.x)
        Start_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rect)
        
    def in_motion(event):
        global Start_X,Start_Y,cur_X,cur_Y,rect,image_on_canvas
        cur_X = img_canvas.canvasx(event.x)
        cur_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rect)
        rect= img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='red')
        img_canvas.tag_raise(rect,image_on_canvas)

    def on_release(event):
        global Start_Y,Start_X,cur_Y,cur_X,pillow_image,pillow_image_copy,image_on_canvas,resized_image_tk,rect
        ht_ratio = resized_image_tk.height()/pillow_image_copy.size[1]
        wd_ratio = resized_image_tk.width()/pillow_image_copy.size[0]
        crp_x1 = Start_X/wd_ratio
        crp_y1 = Start_Y/ht_ratio
        crp_x2 = cur_X/wd_ratio
        crp_y2 = cur_Y//ht_ratio
        rect = img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='red')
        img_canvas.tag_raise(rect,image_on_canvas)
        
        pillow_image_copy = pillow_image_copy.crop((crp_x1,crp_y1,crp_x2,crp_y2))
        resized_image_tk = resize(pillow_image_copy)
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)

    rect = img_canvas.create_rectangle(0,0,1,1,outline='red')
    img_canvas.tag_raise(rect,image_on_canvas)

    img_canvas.bind("<ButtonPress-1>",on_press)
    img_canvas.bind("<B1-Motion>",in_motion)
    img_canvas.bind("<ButtonRelease-1>",on_release)

button_crop = Button(frame_right,text="Select Area to Crop",bg="black",command=select_area,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
button_crop.grid(row=7,columnspan=2,padx=10,pady=10)

def invert():
    global pillow_image,pillow_image_copy
    global resized_image_tk
    global image_on_canvas
    global canvas_width, canvas_height
    
    pillow_image_copy = ImageChops.invert(pillow_image_copy)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
button_invert = Button(frame_right,text="Invert Colours",bg="black",command=invert,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
button_invert.grid(row=9,column=1,padx=10,pady=10)

def apply_changes():
    global pillow_image,pillow_image_copy,image_tk,resized_image_tk,image_on_canvas,canvas_width,canvas_height
    rotate_.set(0)
    bright_.set(10)
    contrast_.set(8)
    sharpen_.set(4)
    sat_.set(10)
    pillow_image = pillow_image_copy
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
apply_change_button = Button(frame_right,text="Apply Changes",bg="black",command=apply_changes,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
apply_change_button.grid(row=10,column=0,padx=10,pady=10)


def save_file():
    global pillow_image
    file_name = filedialog.asksaveasfile(mode='w', defaultextension=".jpeg", filetypes=[("JPG File",".jpg"),("PNG File",".png"),("JPEG File",".jpeg")])
    if not file_name:
        return
    pillow_image.save(file_name)

button_save = Button(frame_right,text="Save this image",bg="black",command=save_file,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=10,pady=5,relief=RAISED,state='disabled')
button_save.grid(row=10,column=1,padx=10,pady=10)

root.mainloop()