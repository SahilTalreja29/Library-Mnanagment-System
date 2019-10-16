from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from databasehelper import *
from DefaultPage import *
from adminpage import *
from customerpage import *

class MainPage(DefaultPage):
    def __init__(self,root):
        super().__init__(root)
        self.add_widgets()

    def getLoginScreen(self,login_type):
        login_window=Toplevel()
        f=Frame(login_window,height=200,width=400)
        l1 = Label(f, width=20, text="Enter username: ")
        self.e1 = Entry(f, width=30, fg='black', bg='white')
        self.e1.focus_set()
        self.e2 = Entry(f, width=30, fg='black', bg='white', show='*')
        l2 = Label(f, width=20, text="Enter password: ")
        l1.grid(row=1, column=1, padx=10, pady=10)
        l2.grid(row=2, column=1, padx=10, pady=10)
        self.e1.grid(row=1, column=4, padx=10, pady=10)
        self.e2.grid(row=2, column=4, padx=10, pady=10)
        b1 = Button(f, text="Submit", height=2, width=10, command=lambda: self.validate(self.root,login_window,login_type))
        b1.grid(row=3, column=1, padx=10, sticky='e')
        b2 = Button(f, text="Reset", height=2, width=10, command=lambda: self.reset())
        b2.grid(row=3, column=4, padx=10, sticky='w')
        f.pack()
        f.grid_propagate(0)

    def reset(self):
        self.e1.delete(0,END)
        self.e2.delete(0, END)

    def add_widgets(self):
        self.admin_button = Button(self.panel, text="Admin login", command=lambda: self.getLoginScreen("Admin"), width=20,height=2, activebackground="gray")
        self.admin_button.place(x=450, y=150)
        self.user_button = Button(self.panel, text="User login", command=lambda: self.getLoginScreen("User"), width=20,height=2, activebackground="gray")
        self.user_button.place(x=620, y=150)
        self.new_user_button = Button(self.panel, text="New user? Sign up here", width=20, height=2,activebackground="gray", activeforeground="white", borderwidth=2, relief=RIDGE,command=self.sign_up_form)
        self.new_user_button.place(x=550, y=220)

    def sign_up_form(self):
        text_font = ("MS Serif", 12)
        registration_window=Toplevel()
        f=Frame(registration_window,width=650,height=400,bg="white")
        Message(f, font="Roman 20 bold", text="Vesit Library Services", width=300).grid(row=0, column=0,columnspan=3, pady=5)
        Message(f, text="Register with us to get the best of books experience", width=600,font="Roman 20 bold italic",bg="white", relief=SOLID,borderwidth=2).grid(row=1,column=0,columnspan=3)
        f.pack()
        l=Label(f,text="Name",font=text_font)
        l.grid(row=2,column=0,padx=10,pady=10)
        self.register_e1=Entry(f)
        self.register_e1.grid(row=2,column=1,padx=10,pady=10)
        self.register_e1.focus_set()
        l=Label(f,text="Contact",font=text_font)
        l.grid(row=3, column=0, padx=10, pady=10)
        self.register_e2 = Entry(f)
        self.register_e2.grid(row=3, column=1, padx=10, pady=10)
        l = Label(f, text="Email Id",font=text_font)
        l.grid(row=4, column=0, padx=10, pady=10)
        self.register_e3 = Entry(f)
        self.register_e3.grid(row=4, column=1, padx=10, pady=10)
        l = Label(f, text="Password",font=text_font)
        l.grid(row=5, column=0, padx=10, pady=10)
        self.register_e4 = Entry(f,show="*")
        self.register_e4.grid(row=5, column=1, padx=10, pady=10)
        l = Label(f, text="Re-enter Password",font=text_font)
        l.grid(row=6, column=0, padx=10, pady=10)
        self.register_e5 = Entry(f,show="*")
        self.register_e5.grid(row=6, column=1, padx=10, pady=10)
        b1=Button(f,text="Register", width=20, height=2, bg="white", fg="black",activebackground="gray",command=lambda: self.register_user(registration_window))
        b1.grid(row=7,column=0,padx=10,pady=10,sticky="e")
        b2 = Button(f, text="Reset", width=20, height=2, bg="white", fg="black",activebackground="gray",command=self.register_reset)
        b2.grid(row=7, column=1, padx=10, pady=10,sticky="w")
        f.grid_propagate(0)

    def register_reset(self):
        self.register_e1.delete(0,END)
        self.register_e2.delete(0, END)
        self.register_e3.delete(0, END)
        self.register_e4.delete(0, END)
        self.register_e5.delete(0, END)

    def register_user(self,registration_window):
        name=self.register_e1.get()
        contact=self.register_e2.get()
        email=self.register_e3.get()
        pwd=self.register_e4.get()
        pwd2=self.register_e5.get()
        if(name=="" or contact=="" or email=="" or pwd==""):
            messagebox.showwarning("Mandatory fields","Please fill all the fields")
            registration_window.focus_set()
        elif(pwd!=pwd2):
            messagebox.showerror("Password Error","Passwords don't match.Please re-enter")
            registration_window.focus_set()
        else:
            query="Insert into Customer(CustomerName, CustomerPassword, CustomerEmail) Values ('%s','%s','%s')"
            args=(name,pwd,email)
            DatabaseHelper.execute_query(query,args)
            messagebox.showinfo("Success","User registered successfully. Please login")
            registration_window.destroy()

    def validate(self,root,login_window,login_type):
        username=self.e1.get()
        pwd = self.e2.get()
        if(login_type=="Admin"):
            query = "Select * from world.Admin where AdminName= '%s' and AdminPassword='%s'"
        else:
            query = "Select * from world.Customer where CustomerName= '%s' and CustomerPassword='%s'"
        parameters=(username,pwd)
        result=DatabaseHelper.get_data(query,parameters)
        if(result is None or len(result)==0):
            messagebox.showerror("Login Failed","Incorrect credentials")
        else:
            messagebox.showinfo('Login Success',"Login successfuly completed")
            login_window.destroy()
            self.f.destroy()
            self.panel.destroy()
            if(login_type=="Admin"):
                self.redirect=AdminHomePage(root,result)
            else:
                self.redirect=CustomerHomePage(root,result)
        print(username)
        print(pwd)

root=Tk()
root.geometry('900x600')
root.title("Welcome to Vesit Library Services. The best books you'll ever get")
l=MainPage(root)
root.mainloop()