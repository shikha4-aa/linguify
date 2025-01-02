import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vinayak@23",  # Replace with your MySQL password
    database="LINGUIFY"  # Replace with your database name
)
cur = db.cursor()

# Function to retrieve teaching data from the database
def get_teaching_data(language_id, session_number):
    query = """
        SELECT word, translation, image
        FROM Teaching
        WHERE language_id = %s AND session_number = %s
    """
    cur.execute(query, (language_id, session_number))
    data = cur.fetchall()

    # Debugging: Check if the image data is retrieved correctly
    for row in data:
        print(f"Word: {row[0]}, Translation: {row[1]}, Image data type: {type(row[2])}, Image length: {len(row[2]) if row[2] else 'None'}")
    
    return data

def insert_image(language_id, session_number, word, translation, image_path):
    with open(image_path, 'rb') as file:
        binary_image = file.read()

    query = "INSERT INTO Teaching (language_id, session_number, word, translation, image) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (language_id, session_number, word, translation, binary_image))
    db.commit()


# Function to display Spanish translation
def show_translation(word, translation):
    messagebox.showinfo("Translation", f"{word} in Spanish is '{translation}'")

# Function to display words and images on the Tkinter GUI
def display_teaching_session(language_id, session_number):
    root = Tk()
    root.title(f"Session {session_number} - Language Learning")
    root.geometry("800x600")

    data = get_teaching_data(language_id, session_number)

    if not data:
        messagebox.showerror("No Data", "No words or images found for this session.")
        return

    row = 0
    for word, translation, img_data in data:
        # Create a label for the word
        word_label = Label(root, text=word, font=("Arial", 16), cursor="hand2")
        word_label.grid(row=row, column=0, padx=20, pady=20)
        
        # Bind the click event to show the translation when the word is clicked
        word_label.bind("<Button-1>", lambda e, w=word, t=translation: show_translation(w, t))

        # Convert binary image data to a format that Tkinter can use
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((100, 100))  # Resize image if necessary
        tk_img = ImageTk.PhotoImage(img)

        # Create a button with the image
        image_button = Button(root, image=tk_img, borderwidth=0, cursor="hand2")
        image_button.image = tk_img  # Store a reference to avoid garbage collection
        image_button.grid(row=row, column=1, padx=20, pady=20)
        
        # Bind the click event to show the translation when the image is clicked
        image_button.bind("<Button-1>", lambda e, w=word, t=translation: show_translation(w, t))

        row += 1

    root.mainloop()

# Example: Display session 1 for Spanish (language_id = 4)
display_teaching_session(language_id=4, session_number=1)

# Close the database connection
cur.close()
db.close()
