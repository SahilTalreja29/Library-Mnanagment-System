from DefaultPage import *
from tkinter import messagebox

class CustomerHomePage(DefaultPage):
    def __init__(self,root,customer_details):
        print("Admin home page called")
        self.customer_details=customer_details
        self.text_font = ("Comic sans ms", 12)
        self.dct_IntVar = {}
        super().__init__(root)
        self.m = Message(self.panel, width=600, font="Roman 20 bold italic",
                         text="Customer Page", bg="white", relief=SOLID
                         , borderwidth=2)
        self.m.place(x=320, y=20)
        self.add_menu()

    def add_menu_items(self,menu_type):
        self.menu_b5 = Button(self.menu_frame, text="Place Order", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=self.place_order)
        self.menu_b5.place(x=350,y=10)
        self.menu_items_frame=Frame(self.menu_frame,height=350,width=350)
        self.menu_items_frame.place(x=50,y=50)
        self.diary2_img = ImageTk.PhotoImage(Image.open("Diary2.jpg"))
        self.diary2_panel = Label(self.menu_items_frame, image=self.diary2_img)
        self.diary2_panel.pack()
        self.diary2_panel.pack_propagate(0)
        result=self.get_menu(menu_type)
        print(result)
        for i in range(len(result)):
            self.dct_IntVar[result[i][1]]=IntVar()
        self.menu_frame.pack_propagate(0)
        for i in range(len(result)):
            Checkbutton(self.menu_items_frame,text=result[i][0],font=self.text_font,variable=self.dct_IntVar.get(result[i][1])).place(x=50,y=30+40*i)
            Label(self.menu_items_frame,text=result[i][1],font=self.text_font).place(x=100,y=30+40*i)
            Label(self.menu_items_frame,text=result[i][2],font=self.text_font).place(x=300,y=30+40*i)

    def place_order(self):
        selected_items=[]
        for key,value in self.dct_IntVar.items():
            if(value.get()==1):
                selected_items.append(key)
        print(selected_items)
        if(len(selected_items)==0):
            messagebox.showwarning("No books","Please select atleast one book")
            return
        query="Select BookssAuthor from world.BookssMenu where BookssName in (%s)"
        res=DatabaseHelper.get_all_data_multiple_input(query,selected_items)
        print(res)
        self.order_confirmation(selected_items,res)

    def order_confirmation(self,selected_items,res):
        confirmation_window = Toplevel()
        f = Frame(confirmation_window, height=200, width=400)
        f.pack()
        purchased_items="\n".join(selected_items)
        #total=0
        #for item in res:
            #total+=item[0]
        message=f"The items purchased are \n {purchased_items} \n"
        l=Label(f,text=message)
        l.grid(row=1,column=0,columnspan=2)
        b1 = Button(f, text="Confirm", height=2, width=10,
                    command=lambda :self.send_order_to_admin(selected_items,confirmation_window))
        b1.grid(row=3, column=0, padx=10, sticky='e')
        b2 = Button(f, text="Reset", height=2, width=10)
        b2.grid(row=3, column=1, padx=10, sticky='w')
        f.grid_propagate(0)
    def get_menu(self,menu_type):
        query="Select BookssMenuId,BookssName,BookssAuthor from world.BookssMenu where BookssType='%s'"
        args=(menu_type,)
        result=DatabaseHelper.get_all_data(query,args)
        return result

    def send_order_to_admin(self,order_list,window):
        print(order_list)
        food_details=",".join(order_list)
        #print(total)
        print(self.customer_details)
        query="Insert into FoodOrder(CustomerId,FoodDetails) Values(%d,'%s')"
        args=(self.customer_details[0],food_details)
        DatabaseHelper.execute_query(query,args)
        window.destroy()
        messagebox.showinfo("Success","Thank you for placing the order with us.")

    def view_order_status(self):
        query="Select * from world.FoodOrder where IsComplete=0 and CustomerId=%d"
        args=(self.customer_details[0],)
        result=DatabaseHelper.get_data(query,args)
        if(result is None or len(result)==0):
            messagebox.showinfo("No order","You do not have any pending order with us.")
        else:
            details=result[2]
            #total=result[3]
            message=f"Your order for {details} is with us.Should be given soon"
            messagebox.showinfo("Pending order",message)

    def add_menu(self):
        self.menu_frame=Frame(self.panel,height=450,width=450,bg="white")
        self.menu_frame.place(x=400,y=110)
        self.menu_frame.pack_propagate(0)
        self.menu_img = ImageTk.PhotoImage(Image.open('MenuBackground2.png'))
        self.menu_panel = Label(self.menu_frame, image=self.menu_img)
        #self.menu_message = Message(self.menu_frame, width=600, font="Roman 20 bold italic",text="Menu", bg="white", relief=SOLID, borderwidth=2)
        #self.menu_message.place(x=200, y=10)

#        self.check_buttons=[]
        self.menu_b1 = Button(self.menu_frame, text="Engg. Books", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=lambda :self.add_menu_items("Engg. Books"))
        self.menu_b1.place(x=50,y=400)
        self.menu_b2 = Button(self.menu_frame, text="Comic Books", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=lambda :self.add_menu_items("Comic Books"))
        self.menu_b2.place(x=200,y=400)
        self.menu_b3 = Button(self.menu_frame, text="Horror Books", width=10, height=2, bg="ivory2", fg="black",activebackground="white",command=lambda :self.add_menu_items("Horror Books"))
        self.menu_b3.place(x=350,y=400)

        self.menu_b4 = Button(self.menu_frame, text="View Book Status", width=15, height=2, bg="ivory2", fg="black",activebackground="white",command=self.view_order_status)

        self.menu_b4.place(x=30,y=10)
        self.menu_panel.pack()
        self.menu_panel.grid_propagate(0)


if __name__ == '__main__':
    root=Tk()
    c=CustomerHomePage(root,(1,2,3,4))
    root.mainloop()