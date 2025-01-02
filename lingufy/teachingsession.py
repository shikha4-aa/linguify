import mysql.connector
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import io

# Function to retrieve all images, words, and translations from the database
def retrieve_images():
    conn = mysql.connector.connect(host='localhost', user='root', password='Vinayak@23', database='LINGUIFY')
    cursor = conn.cursor()

    # SQL query to select word, translation, and image for all records
    sql = "SELECT word, translation, image FROM images WHERE word_id BETWEEN 1 AND 10"
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

# Function to display all images, words, and translation buttons in a 5x2 grid
def display_images():
    results = retrieve_images()
    
    positions = [
        (50, 100), (450, 100),  (900, 100), 
        (50, 300), (450, 300), (900, 300),   # Row 3
        (50, 500), (450, 500), (900, 500), (400, 700)    # Row 5
    ]
    if results:
        # Iterate over all rows fetched from the database
        for idx, (word, translation, image_data) in enumerate(results):
            if image_data:
                # Convert image blob data to PIL Image
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((150, 120), Image.Resampling.LANCZOS)  # Resize image to 150x120
                photo = ImageTk.PhotoImage(image)


                x_pos, y_pos = positions[idx] # Calculate row and column position for 5x2 grid (2 items per row)
                # Multiply by 3 for image, word, and button placement

                # Display the image
                label_image = Label(root, image=photo)
                label_image.image = photo  # Keep a reference to the image
                label_image.place(x=x_pos, y=y_pos)

                # Display the word
                label_word = Label(root, text=word, font=("Arial", 14, "bold"))
                label_word.place(x=x_pos, y=y_pos + 150)

                # Label for displaying translation (initially empty)
                label_translation = Label(root, text="", font=("Arial", 12))
                label_translation.place(x=x_pos, y=y_pos + 180)

                # Function to show translation on button click
                def show_translation(lbl, trans=translation):
                    lbl.config(text=trans)

                # Translate button with image
                translate_img = ImageTk.PhotoImage(Image.open("./images/translate_button.png"))
                btn_translate = Button(root, image=translate_img, command=lambda lbl=label_translation: show_translation(lbl), bg='white', borderwidth=0)
                btn_translate.image = translate_img  # Keep a reference to the image
                btn_translate.place(x=x_pos + 220, y=y_pos + 50)  # Place the button next to the image
    else:
        print("No images found.")

# Tkinter setup
root = tk.Tk()
root.title("Image Viewer")
root.geometry("1366x768")  # Set window size

# Load the background image
bg_image = Image.open("images/teaching_page.png")  # Replace with the path to your background image
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
background_label = Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)  # Place it to cover the entire window

# Call the function to display all images and their corresponding words and translations
display_images()

# Start the Tkinter main loop
root.mainloop() 
