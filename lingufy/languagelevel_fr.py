import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os

level_selection_window = Tk()
level_selection_window.geometry("1366x768")

def save_language_level(username, level, db, cur):
    try:
        # Update the User's level in the database
        cur.execute("UPDATE User SET user_level = %s WHERE username = %s", (level, username))
        db.commit()

        # Confirmation message after successful update
        messagebox.showinfo("Success", f"You have selected {level} level.")

        # Start the appropriate quiz based on the selected level
        
        if level == "Intermediate":
            start_quiz_page_fr_inter(username)
        elif level == "Advanced":
            start_quiz_page_fr_adv(username)
        elif level == "Beginner":
            start_quiz_page_fr_adv(username)

        level_selection_window.destroy()  # Close the current window

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function definitions for starting quizzes

def start_quiz_page_fr_inter(username):
    os.system("python french_intermediate.py")

def start_quiz_page_fr_adv(username):
    os.system("python french_advanced.py")

def start_quiz_page_fr_adv(username):
    os.system("python french_beginner.py")

def show_language_level_selection(username):
    level_selection_window.title("Select Your French Proficiency Level")

    # Load and display the background image
    img_bg = Image.open("./images/languagelevel.png")
    bg_image = ImageTk.PhotoImage(img_bg)
    background_label = Label(level_selection_window, image=bg_image)
    background_label.place(relx=0, rely=0, width=1366, height=768)

    try:
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinayak@23",
            database="LINGUIFY"
        ) as db:
            cur = db.cursor()

            # Add buttons with image references
            beginner_img = PhotoImage(file="./images/beginner_button.png")
            beginner_button = Button(level_selection_window, image=beginner_img, borderwidth=0, 
                                     command=lambda: save_language_level(username, "Beginner", db, cur))
            beginner_button.image = beginner_img
            beginner_button.place(x=340, y=158, width=490, height=90)
            
            intermediate_img = PhotoImage(file="./images/intermediate_button.png")
            intermediate_button = Button(level_selection_window, image=intermediate_img, borderwidth=0, 
                                         command=lambda: save_language_level(username, "Intermediate", db, cur))
            intermediate_button.image = intermediate_img
            intermediate_button.place(x=338, y=360, width=492, height=93)
            
            advanced_img = PhotoImage(file="./images/advanced_button.png")
            advanced_button = Button(level_selection_window, image=advanced_img, borderwidth=0, 
                                     command=lambda: save_language_level(username, "Advanced", db, cur))
            advanced_button.image = advanced_img
            advanced_button.place(x=338, y=563, width=492, height=93)

            level_label = Label(level_selection_window, text="How familiar are you with Spanish?", font=("Times", 35 , "bold"), bg="white")
            level_label.place(x=220, y=40)

            # Add Logout button
            logout_image = PhotoImage(file="./images/logout_button.png")
            logout_button = Button(level_selection_window, image=logout_image, borderwidth=0,
                                   command=lambda: logout(level_selection_window, db))
            logout_button.image = logout_image
            logout_button.place(x=1185, y=705)

            level_selection_window.mainloop()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def logout(level_selection_window, db):
    messagebox.showinfo("Logout", "You have been logged out.")
    level_selection_window.destroy()
    os.system("python login_page.py")

# Test with a sample username
if __name__ == "__main__":
    username = "test_user"  # Replace with actual username after login
    show_language_level_selection(username)
