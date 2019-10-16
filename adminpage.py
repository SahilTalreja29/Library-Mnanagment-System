from DefaultPage import *

class AdminHomePage(DefaultPage):
    def __init__(self,root,admin_details):
        print("Admin home page called")
        self.details=admin_details
        self.dct_IntVar = {}
        super().__init__(root)
        self.m = Message(self.panel, width=600, font="Roman 20 bold italic",
                         text="Admin Page", bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=320, y=20)
        self.add_admin_details()
        self.add_buttons()

    def execute_order(self):
        selected_items = []
        for key, value in self.dct_IntVar.items():
            if (value.get() == 1):
                print(f"Key is {key}")
                selected_items.append(str(key))
        print(selected_items)
        if (len(selected_items) == 0):
            messagebox.showwarning("No book", "Please select atleast one book to execute")
            return
        query="Update world.FoodOrder Set IsComplete=1 where FoodOrderId in (%s)"
        DatabaseHelper.execute_all_data_multiple_input(query,selected_items)
        messagebox.showinfo("Success","Orders executed")
        self.view_pending_orders()

    def add_menu_frame(self):
        self.menu_frame = Frame(self.f, height=420, width=450)
        self.menu_frame.place(x=400, y=140)
        self.img_diary = ImageTk.PhotoImage(Image.open("DiaryAdmin.jpg"))
        self.diary_panel = Label(self.menu_frame, image=self.img_diary, width=450, height=420)
        self.diary_panel.pack()
        self.diary_panel.pack_propagate(0)
        self.menu_frame.pack_propagate(0)

    def view_completed_orders(self):
        self.add_menu_frame()
        query="Select * from world.FoodOrder where IsComplete=1 order by FoodOrderId limit 5"
        result=DatabaseHelper.get_all_data(query)
        self.text_font=("MS Serif",12)
        for i in range(len(result)):
            self.dct_IntVar[result[i][0]]=IntVar()
        Label(self.menu_frame, font="Times 12", text="CustomerId").grid(row=1, column=1,pady=10)
        Message(self.menu_frame, font="Times 12", text="FoodItems", width=300).grid(row=1, column=2,sticky="w",pady=10)
        for i in range(len(result)):
            Label(self.menu_frame,font=self.text_font,text=result[i][1]).grid(row=i+2,column=1,pady=5)
            Message(self.menu_frame,font=self.text_font,text=result[i][2],width=300).grid(row=i+2,column=2,sticky="w",pady=5)
        self.menu_frame.grid_propagate(0)


    def view_pending_orders(self):
        self.add_menu_frame()
        self.execute_button=Button(self.menu_frame, text="Execute Order", width=20, height=2, bg="white", fg="black",activebackground="gray",command=self.execute_order)
        self.execute_button.grid(row=0,column=0,columnspan=2,sticky="e")
        query="Select * from world.FoodOrder where IsComplete=0"
        result=DatabaseHelper.get_all_data(query)
        self.text_font=("MS Serif",12)
        for i in range(len(result)):
            self.dct_IntVar[result[i][0]]=IntVar()
        Label(self.menu_frame, font="Times 12", text="CustomerId").grid(row=1, column=1,pady=10)
        Message(self.menu_frame, font="Times 12", text="FoodItems", width=300).grid(row=1, column=2,sticky="w",pady=10)
        for i in range(len(result)):
            Checkbutton(self.menu_frame,text=result[i][0],font=self.text_font,variable=self.dct_IntVar.get(result[i][0])).grid(row=i+2,column=0)
            Label(self.menu_frame,font=self.text_font,text=result[i][1]).grid(row=i+2,column=1,pady=5)
            Message(self.menu_frame,font=self.text_font,text=result[i][2],width=300).grid(row=i+2,column=2,sticky="w",pady=5)
        self.menu_frame.grid_propagate(0)

    def add_buttons(self):
        self.pending_button = Button(self.f, text="View Pending Books", width=20, height=2, bg="white", fg="black",activebackground="gray",command=self.view_pending_orders)
        self.pending_button.place(x=400, y=90)
        self.completed_button = Button(self.f, text="View Recent Completed Books", width=25, height=2, bg="white", fg="black",activebackground="gray",command=self.view_completed_orders)
        self.completed_button.place(x=550, y=90)

    def add_admin_details(self):
        print(self.details)
        self.profile_pic = ImageTk.PhotoImage(Image.open(self.details[4]))
        self.c=Canvas(self.panel,width=100,height=180)
        #self.photo_l= Label(self.f, image=self.img)
        self.canvas_pic=self.c.create_image(0,0,image=self.profile_pic,anchor=NW)
        self.c.place(x=40,y=100)
        self.panel.pack()
        self.panel.pack_propagate(0)
        self.m = Message(self.f, width=150, font="Roman 15 italic",
                         text="Name= "+self.details[1], bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=40, y=300)
        self.m = Message(self.f, width=250, font="Roman 15 italic",
                         text="Email"+self.details[3], bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=40, y=350)

if __name__ == '__main__':
    root=Tk()
    a=AdminHomePage(root,(2, 'Sahil', 'sahil', 'sahil@gmail.com', 'RiteshPic3.jpg'))
    root.mainloop()