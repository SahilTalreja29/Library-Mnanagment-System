from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from databasehelper import *
class DefaultPage:
    def __init__(self,root):
        self.root=root
        self.root.iconbitmap('FoodIcon.ico')
        self.f=Frame(root,height=600,width=900)
        self.f.pack()
        self.img = ImageTk.PhotoImage(Image.open("foodBackground2.jpg"))
        self.panel = Label(self.f, image=self.img)
        self.panel.pack()
        self.panel.pack_propagate(0)
        self.m = Message(self.f, width=600, font="Roman 20 bold italic",
                         text="Vesit Library services",bg="white",relief=SOLID
                         ,borderwidth=2)
        self.m.place(x=520, y=20)
        self.footer=Label(self.panel,bg="ivory3",height=1,text="@Copyright 2019 Vesit Library services. All rights reserved")
        self.footer.pack_propagate(0)
        self.footer.pack(side=BOTTOM,fill=X)
        self.f.pack_propagate(0)



