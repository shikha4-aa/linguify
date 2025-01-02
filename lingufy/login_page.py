import mysql.connector 
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst

root = Tk()
root.geometry("1366x768")
root.title("LINGUFY LOGIN")

user = StringVar()
passwd = StringVar()

class login_page:
    def __init__(self, top=None):
        self.root = top  # Store the root window
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("LINGUFY LOGIN PAGE")

        self.label1 = Label(top)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/learner_login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(top, font="-family {Poppins} -size 15", relief="flat", textvariable=user)
        self.entry1.place(x=545, y=320, width=303, height=30)


        self.entry2 = Entry(top, font="-family {Poppins} -size 15", relief="flat", show="*", textvariable=passwd)
        self.entry2.place(x=545, y=443, width=302, height=30)

        login_image = PhotoImage(file="./images/login_button.png")
        self.button1 = Button(top, image=login_image, relief="flat", activebackground="#8B17F7",
                              cursor="hand2", background="#8B17F7", borderwidth="0", command=self.login)
        self.button1.place(x=582, y=523, width=196.26, height=63)
        self.button1.image = login_image

        create_image = PhotoImage(file="./images/create_fin.png")
        self.button2 = Button(top, image=create_image, relief="flat", activebackground="#8B17F7",
                              cursor="hand2", background="#8B17F7", borderwidth="0", command=self.create_account)
        self.button2.place(x=748.29, y=626, width=114.16, height=36)
        self.button2.image = create_image

    def login(self, event=None):
        username = user.get()
        password = passwd.get()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinayak@23",
                database="LINGUIFY"
            )
            cur = db.cursor()
            cur.execute("SELECT password FROM User WHERE username = %s", (username,))
            result = cur.fetchone()
            if result and password == result[0]:  # Use hashed password for real scenarios
                messagebox.showinfo("Login Page", "The login is successful")
                self.entry1.delete(0, END)
                self.entry2.delete(0, END)
                self.root.withdraw()
                os.system("python language_selection.py")
                root.deiconify()
                
               
            else:
                messagebox.showerror("Error", "Incorrect username or password.")
                self.entry2.delete(0, END)
                db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            if 'db' in locals():
                db.close()

    def create_account(self):
        self.root.withdraw()  # Hide the login page
        global account_creation
        account_creation = Toplevel()
        account_creation_page(account_creation)


class account_creation_page:
    def __init__(self, top=None):
        self.new_user = StringVar()
        self.new_passwd = StringVar()
        self.new_confirmpass = StringVar()

        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("LINGUFY - Create New Account")

        self.label1 = Label(top)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/create_page.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(top, font="-family {Poppins} -size 15", relief="flat", textvariable=self.new_user)
        self.entry1.place(x=535, y=283, width=320, height=30)

        self.entry2 = Entry(top, font="-family {Poppins} -size 15", relief="flat", show="*", textvariable=self.new_passwd)
        self.entry2.place(x=535, y=400, width=320, height=28)

        self.entry3 = Entry(top, font="-family {Poppins} -size 15", relief="flat", show="*", textvariable=self.new_confirmpass)
        self.entry3.place(x=535, y=510, width=320, height=28)

        create_page = PhotoImage(file="./images/create_button.png")
        self.button1 = Button(top, image=create_page, relief="flat", activebackground="#8B17F7",
                              cursor="hand2", background="#8B17F7", borderwidth="0", command=self.submit_new_account)
        self.button1.place(x=582, y=582, width=196.26, height=61.04)
        self.button1.image = create_page

    def submit_new_account(self):
        if self.new_passwd.get() != self.new_confirmpass.get():
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            with mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinayak@23",
                database="LINGUIFY"
            ) as db:
                cur = db.cursor()
                cur.execute("SELECT username FROM User WHERE username = %s", (self.new_user.get(),))
                if cur.fetchone():
                    messagebox.showerror("Error", "Username already exists.")
                    return

                cur.execute("INSERT INTO User (username, password) VALUES (%s, %s)",
                            (self.new_user.get(), self.new_passwd.get()))
                db.commit()
            messagebox.showinfo("Account Creation", "Account created successfully!")
            account_creation.destroy()  # Close the account creation window
            root.deiconify()  # Show the login page again
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

page1 = login_page(root)
root.bind("<Return>", page1.login)
root.mainloop()
