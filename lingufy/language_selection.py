import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os

language_selection_window = Tk()
language_selection_window.geometry("1366x768")

def show_language_selection(username):
    language_selection_window.title("Select the Language to Learn")

    # Load and display the background image
    background_label = Label(language_selection_window)
    background_label.place(relx=0, rely=0, width=1366, height=768)
    img_bg = PhotoImage(file="./images/lang_selectpg.png")  # Use your own background image path
    background_label.configure(image=img_bg)

    # Languages list
    languages = ["English", "Spanish", "French"]

    y_position = 200

    try:
        # Connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinayak@23",
            database="LINGUIFY"
        )
        cur = db.cursor()

        # Loop to display each 'Select' button for languages
        for lang in languages:
            select_image = PhotoImage(file="./images/select_button.png")  # Use your select button image
            button = Button(language_selection_window, image=select_image, borderwidth=0,
                            command=lambda l=lang: submit_language_choice(username, l, db, cur))
            button.image = select_image
            button.place(x=882, y=y_position + 15)

            y_position += 187

        # Load the Logout button image
        logout_image = PhotoImage(file="./images/logout_button.png")  # Provide the path to your logout button image
        logout_button = Button(language_selection_window, image=logout_image, borderwidth=0,
                               command=lambda: logout(language_selection_window, db))
        logout_button.image = logout_image
        logout_button.place(x=1185, y=705)

        language_selection_window.mainloop()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'db' in locals():
            db.close()

def submit_language_choice(username, selected_language, db, cur):
    try:
        # Fetch the language ID from the Language table based on the selected language name
        cur.execute("SELECT language_id FROM Language WHERE language_name = %s", (selected_language,))
        language_id = cur.fetchone()

        # Ensure to fetch any remaining results to clear the cursor
        cur.fetchall()

        if language_id:
            # Update the User's current_language in the database with the chosen language ID
            cur.execute("UPDATE User SET current_language = %s WHERE username = %s", (language_id[0], username))
            db.commit()

            # Confirmation message after successful update
            messagebox.showinfo("Success", f"You have selected {selected_language} as the language to learn.")
            language_selection_window.withdraw()

            if selected_language == "English":
                os.system("python languagelevel_eng.py")  # For English
            elif selected_language == "Spanish":
                os.system("python languagelevel_esp.py")  # For Spanish
            elif selected_language == "French":
                os.system("python languagelevel_fr.py") 
             # Call the next page
            language_selection_window.deiconify()
        else:
            messagebox.showerror("Error", f"Language {selected_language} not found in the database.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def logout(language_selection_window, db):
    messagebox.showinfo("Logout", "You have been logged out.")
    language_selection_window.destroy()  # Close the language selection window
    # Optionally, you can call the login screen again if needed

# For testing purposes, pass a sample username
if __name__ == "__main__":
    username = "test_user"  # Replace with actual username after login
    show_language_selection(username)
