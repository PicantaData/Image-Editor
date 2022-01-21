def onClick():
    my_label = Label(frame_right, text="Hello User!")
    my_label.grid(row="5",column="5")

my_button = Button(frame_right,text="Say Hello!",command = onClick,bg="black",fg="white",activebackground="white",activeforeground="black")
my_button.grid(row="2",column="5")