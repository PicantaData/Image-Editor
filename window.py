from logging import root
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog

root = Tk()
root.title('Image Editor')
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry(f"{width}x{height}")

#Converting jpg image to .ico and placing it on title window
to_convert = Image.open('image-editing-icon.jpg')
converted_pic = ImageTk.PhotoImage(to_convert)
root.wm_iconphoto(False, converted_pic)


frame_left = LabelFrame(root,bg="lightgreen",padx=10,pady=10,width=1000,height=705)
frame_left.grid(row=0,column=0)
frame_left.grid_propagate(0)

frame_right = LabelFrame(root,bg="lightblue",padx=5,pady=5,width=365,height=705)
frame_right.grid(row=0,column=1)
frame_right.grid_propagate(0)

def import_img():
    global open_image
    frame_left.imgaddress = filedialog.askopenfilename(initialdir="C:/Users/Vrishin/Desktop/woc4_pyImageEditor_vrishin",title="Select an image",filetypes=(("jpg files","*.jpg"),("png files", "*.png"),("jpeg files","*.jpeg")))
    open_image = ImageTk.PhotoImage(Image.open(frame_left.imgaddress))
    open_image_label = Label(frame_left,image=open_image)
    open_image_label.grid(row=0,column=0,padx=10,pady=10)

insert_img_button = Button(frame_left, text="Import Image",command = import_img,bg="black",fg="white",activebackground="white",activeforeground="black",cursor="target",padx=5,pady=5).grid(row=1,column=0)

root.mainloop()