from logging import root
from tkinter import *
from tkinter import filedialog,colorchooser,messagebox
from PIL import ImageTk,Image,ImageChops,ImageEnhance,ImageDraw,ImageFont
import csv

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
    reset_["state"] = NORMAL
    button_text["state"] = NORMAL
    button_certi["state"] = NORMAL
    txt_entry["state"] = NORMAL
    rotate_.set(0)
    bright_.set(10)
    contrast_.set(8)
    sharpen_.set(4)
    sat_.set(10)
    

#IMPORT-BUTTON
def import_img():
    global pillow_image,pillow_image_copy,resized_image_tk,image_on_canvas,canvas_width,canvas_height,add
    
    add = frame_left.imgaddress = filedialog.askopenfilename(initialdir="/",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    
    pillow_image = Image.open(frame_left.imgaddress)
    pillow_image_copy = pillow_image.copy()
    #image_tk = ImageTk.PhotoImage(pillow_image)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    enable()

insert_img_button = Button(frame_right, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED)
insert_img_button.grid(row=0,column=0,columnspan=2,padx=0.35*f_right_width,pady=20)

#EDITING-BUTTONS
#FILTERS
def rotate(var):
    global pillow_image,pillow_image_copy,pillow_image_copy1
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy1 = pillow_image_copy.copy()
    pillow_image_copy1 = pillow_image_copy1.rotate(-rotate_.get(),expand=True,resample=Image.NEAREST)
    resized_image_tk = resize(pillow_image_copy1)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)

rotate_ = Scale(frame_right,from_=-180,to=180,orient=HORIZONTAL,command=rotate,label="Rotate",state='disabled')
rotate_.grid(row=1,column=0,padx=5,pady=10)

def rotate_final():
    global pillow_image,pillow_image_copy,pillow_image_copy1
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image_copy1
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    rotate_.set(0)
   
rotate_final_button = Button(frame_right,text="Update Rotated Image",bg="black",command=rotate_final,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
rotate_final_button.grid(row=1,column=1,padx=5,pady=10)

#FLIP
def flip_left_right():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height

    pillow_image = pillow_image.transpose(Image.FLIP_LEFT_RIGHT)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
flip_lr_button = Button(frame_right,text="Flip Left-Right",bg="black",command=flip_left_right,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
flip_lr_button.grid(row=2,column=0,padx=5,pady=10)

def flip_top_bottom():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
     
    pillow_image = pillow_image.transpose(Image.FLIP_TOP_BOTTOM)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
flip_tb_button = Button(frame_right,text="Flip Top-Bottom",bg="black",command=flip_top_bottom,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
flip_tb_button.grid(row=2,column=1,padx=5,pady=10)

#IMAGE-COLOUR
def greyscale():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image.copy()
    pillow_image_copy = pillow_image_copy.convert('L')
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
button_greyscale = Button(frame_right,text="Grey Scale",bg="black",command=greyscale,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_greyscale.grid(row=3,column=0,padx=5,pady=10)

def invert():
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width, canvas_height
    
    pillow_image = ImageChops.invert(pillow_image)
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
button_invert = Button(frame_right,text="Invert Colours",bg="black",command=invert,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_invert.grid(row=3,column=1,padx=5,pady=10)

#TONE
def contrast(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image.copy()
    img_cont = ImageEnhance.Contrast(pillow_image_copy)
    pillow_image_copy = img_cont.enhance(contrast_.get()/8.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
contrast_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=contrast,label= "Contrast",state='disabled')
contrast_.grid(row=4,column=0,padx=3,pady=10)

def brightness(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image.copy()
    img_bright = ImageEnhance.Brightness(pillow_image_copy)
    pillow_image_copy = img_bright.enhance(bright_.get()/10.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
bright_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=brightness,label= "Brightness",state='disabled')
bright_.grid(row=4,column=1,padx=5,pady=10)

def saturation(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk,image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image.copy()
    img_sat = ImageEnhance.Color(pillow_image_copy)
    pillow_image_copy = img_sat.enhance(sat_.get()/10.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
sat_ = Scale(frame_right,from_=0,to=30,orient=HORIZONTAL,command=saturation,label= "Saturation",state='disabled')
sat_.grid(row=5,column=0,padx=5,pady=10)


def sharpness(var):
    global pillow_image,pillow_image_copy
    global resized_image_tk, image_on_canvas
    global canvas_width,canvas_height
    
    pillow_image_copy = pillow_image.copy()
    img_sharp = ImageEnhance.Sharpness(pillow_image_copy)
    pillow_image_copy = img_sharp.enhance(sharpen_.get()/4.0)
    resized_image_tk = resize(pillow_image_copy)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
sharpen_ = Scale(frame_right,from_=0,to=20,orient=HORIZONTAL,command=sharpness,label="Sharpness",state='disabled')
sharpen_.grid(row=5,column=1,padx=3,pady=10)

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
        crp_y2 = cur_Y/ht_ratio
        rect = img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='red')
        #img_canvas.tag_raise(rect,image_on_canvas)
        
        pillow_image_copy = pillow_image.copy()
        pillow_image_copy = pillow_image_copy.crop((crp_x1,crp_y1,crp_x2,crp_y2))
        resized_image_tk = resize(pillow_image_copy)
        image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)

        img_canvas.unbind("<ButtonPress-1>")
        img_canvas.unbind("<B1-Motion>")
        img_canvas.unbind("<ButtonRelease-1>")

    rect = img_canvas.create_rectangle(0,0,1,1,outline='red')
    img_canvas.tag_raise(rect,image_on_canvas)
    
    img_canvas.bind("<ButtonPress-1>",on_press)
    img_canvas.bind("<B1-Motion>",in_motion)
    img_canvas.bind("<ButtonRelease-1>",on_release)

button_crop = Button(frame_right,text="Select Area to Crop",bg="black",command=select_area,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_crop.grid(row=6,column=1,padx=5,pady=10)

#ADD TEXT
def txt_img():
    ans = messagebox.askyesno("Image Edit Tool", "Draw rectangular area on Image to place your text")
    if ans==1:
        messagebox.showwarning("WARNING!","Your font size depends on the vertical length of rectangular area." )
    else:
        return

    global rec_txt
    def on_press(event):
        global Start_X,Start_Y,rec_txt,image_on_canvas
        Start_X = img_canvas.canvasx(event.x)
        Start_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rec_txt)
        
    def in_motion(event):
        global Start_X,Start_Y,cur_X,cur_Y,rec_txt,image_on_canvas
        cur_X = img_canvas.canvasx(event.x)
        cur_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rec_txt)
        rec_txt= img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='brown')
        img_canvas.tag_raise(rec_txt,image_on_canvas)

    def on_release(event):
        global Start_Y,Start_X,cur_Y,cur_X,pillow_image,pillow_image_copy,image_on_canvas,resized_image_tk,rec_txt
        ht_ratio = resized_image_tk.height()/pillow_image_copy.size[1]
        wd_ratio = resized_image_tk.width()/pillow_image_copy.size[0]
        txt_x1 = Start_X/wd_ratio
        txt_y1 = Start_Y/ht_ratio
        txt_x2 = cur_X/wd_ratio
        txt_y2 = cur_Y/ht_ratio
        rec_txt = img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='brown')
                
        pillow_image_copy = pillow_image.copy()

        txt_font = ImageFont.truetype("arial.ttf",int(txt_y2-txt_y1))
        font_color = colorchooser.askcolor(title="Choose Font Colour")[1]
        txt = txt_entry.get()
        txt_on_img = ImageDraw.Draw(pillow_image_copy)
        txt_on_img.text((txt_x1,txt_y1),txt,(f"{font_color}"),font=txt_font)

        img_canvas.after(50,apply_changes)
        messagebox.showinfo("Image Edit Tool",("Image Updated Successfully!"))
        txt_entry.delete(0,END)
        img_canvas.unbind("<ButtonPress-1>")
        img_canvas.unbind("<B1-Motion>")
        img_canvas.unbind("<ButtonRelease-1>")

    rec_txt = img_canvas.create_rectangle(0,0,1,1,outline='brown')
    img_canvas.tag_raise(rec_txt,image_on_canvas)
    
    img_canvas.bind("<ButtonPress-1>",on_press)
    img_canvas.bind("<B1-Motion>",in_motion)
    img_canvas.bind("<ButtonRelease-1>",on_release)
    

txt_entry = Entry(frame_right,state='disabled')
txt_entry.grid(row=6,column=0,padx=5,pady=5)

button_text = Button(frame_right,text="Add text to Image",bg="black",command=txt_img,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_text.grid(row=7,column=0,padx=5,pady=10)

#GENERATE MULTIPLE CERTIFICATES USING CSV DATA
def gen_certi():
    global val_li_csv,coords,pillow_image,pillow_image_copy
    csv_add = filedialog.askopenfilename(initialdir="/",title="Select an csv file",defaultextension=".csv")
    
    #Open, read and convert csv file to list
    file_csv = open(csv_add)
    val_csv = csv.reader(file_csv)
    val_li_csv = list(val_csv)
    num_of_txt = len(val_li_csv[0])
    print(num_of_txt)
    print(val_li_csv)
    coords = [] #Stores coordinates for placing text
    
    messagebox.showwarning("WARNING!","Your font size depends on the vertical length of rectangular area")
    
    ans = messagebox.askyesno("Generate Certificate", "Draw two rectangular areas on Image to place your texts")
    if ans==1:
        pass
    else:
        return
    #-----
    def save_certi():
        font_col = colorchooser.askcolor(title="Choose colour for font")[1]
        certi_save_add = filedialog.askdirectory(initialdir="C:/Users/")
        for rows in range(len(val_li_csv)):
            pillow_image_copy = pillow_image.copy()
            txt1_font = ImageFont.truetype("arial.ttf",int(coords[0][2]))
            txt2_font = ImageFont.truetype("arial.ttf",int(coords[1][2]))
            txt1 = val_li_csv[rows][0]
            txt2 = val_li_csv[rows][1]
            txt1_on_img = ImageDraw.Draw(pillow_image_copy)
            txt1_on_img.text((coords[0][0],coords[0][1]),txt1,(f"{font_col}"),font=txt1_font)
            txt2_on_img = ImageDraw.Draw(pillow_image_copy)
            txt2_on_img.text((coords[1][0],coords[1][1]),txt2,(f"{font_col}"),font=txt2_font)
            pillow_image_copy.save(certi_save_add + f"/certi_{rows + 1}.jpg")
        
        messagebox.showinfo("Success!",f"Certificated have been generated successfully! Saved in {certi_save_add}")
        reset()
        img_canvas.unbind("<ButtonPress-1>")
        img_canvas.unbind("<B1-Motion>")
        img_canvas.unbind("<ButtonRelease-1>")
    #-------
    def show_pre():
        print(coords)
        pillow_image_copy = pillow_image.copy()
        #preview-sample
        txt1_font = ImageFont.truetype("arial.ttf",int(coords[0][2]))
        txt2_font = ImageFont.truetype("arial.ttf",int(coords[1][2]))
        txt1 = val_li_csv[0][0]
        txt2 = val_li_csv[0][1]
        txt1_on_img = ImageDraw.Draw(pillow_image_copy)
        txt1_on_img.text((coords[0][0],coords[0][1]),txt1,("black"),font=txt1_font)
        txt2_on_img = ImageDraw.Draw(pillow_image_copy)
        txt2_on_img.text((coords[1][0],coords[1][1]),txt2,("black"),font=txt2_font)
        
        pillow_image_copy.show(title="Preview")
        ans2 = messagebox.askyesno("Accept Changes?","Do you want to continue with this implementation?")
        if ans2==1:
            save_certi()
        else:
            return
    #------
    global rec_txt
    def on_press(event):
        global Start_X,Start_Y,rec_txt,image_on_canvas
        Start_X = img_canvas.canvasx(event.x)
        Start_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rec_txt)
            
    def in_motion(event):
        global Start_X,Start_Y,cur_X,cur_Y,rec_txt,image_on_canvas
        cur_X = img_canvas.canvasx(event.x)
        cur_Y = img_canvas.canvasy(event.y)
        img_canvas.delete(rec_txt)
        rec_txt= img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='grey')
        img_canvas.tag_raise(rec_txt,image_on_canvas)

    def on_release(event):
        global Start_Y,Start_X,cur_Y,cur_X,pillow_image,pillow_image_copy,image_on_canvas,resized_image_tk,rec_txt,coords
        ht_ratio = resized_image_tk.height()/pillow_image_copy.size[1]
        wd_ratio = resized_image_tk.width()/pillow_image_copy.size[0]
        txt_x1 = Start_X/wd_ratio
        txt_y1 = Start_Y/ht_ratio
        txt_x2 = cur_X/wd_ratio
        txt_y2 = cur_Y/ht_ratio
        rec_txt = img_canvas.create_rectangle(Start_X,Start_Y,cur_X,cur_Y,outline='grey')
        coords.append([txt_x1,txt_y1,txt_y2-txt_y1]) #coords[t] =[x,y,font_size]; t=0,1,..(columns)
        if len(coords)==2:
            show_pre()

    rec_txt = img_canvas.create_rectangle(0,0,1,1,outline='grey')
    img_canvas.tag_raise(rec_txt,image_on_canvas)
        
    img_canvas.bind("<ButtonPress-1>",on_press)
    img_canvas.bind("<B1-Motion>",in_motion)
    img_canvas.bind("<ButtonRelease-1>",on_release)
    
button_certi = Button(frame_right,text="Generate Certificates",bg="black",command=gen_certi,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_certi.grid(row=7,column=1,padx=5,pady=10)

def apply_changes():
    global pillow_image,pillow_image_copy,resized_image_tk,image_on_canvas,canvas_width,canvas_height
    rotate_.set(0)
    bright_.set(10)
    contrast_.set(8)
    sharpen_.set(4)
    sat_.set(10)
    pillow_image = pillow_image_copy
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)
    
apply_change_button = Button(frame_right,text="Apply Changes",bg="black",command=apply_changes,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
apply_change_button.grid(row=8,column=0,padx=5,pady=10)

def reset():
    global pillow_image,pillow_image_copy,resized_image_tk,image_on_canvas,add

    pillow_image = Image.open(add)
    pillow_image_copy = pillow_image.copy()
    resized_image_tk = resize(pillow_image)
    image_on_canvas = img_canvas.create_image(0,0,anchor=NW,image=resized_image_tk)

reset_ = Button(frame_right, text="Reset to default",command = reset,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
reset_.grid(row=8,column=1,padx=5,pady=20)

def save_file():
    global pillow_image
    file_name = filedialog.asksaveasfile(mode='w', defaultextension=".jpeg", filetypes=[("JPG File",".jpg"),("PNG File",".png"),("JPEG File",".jpeg")])
    if not file_name:
        return
    pillow_image.save(file_name)

button_save = Button(frame_right,text="Save this image",bg="black",command=save_file,fg="white",activebackground="white",activeforeground="black",cursor="hand2",padx=5,pady=5,relief=RAISED,state='disabled')
button_save.grid(row=9,columnspan=2,padx=5,pady=10)

root.mainloop()