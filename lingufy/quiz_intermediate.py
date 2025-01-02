import tkinter as tk
from tkinter import Button, Label, PhotoImage, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vinayak@23",  # Replace with your actual MySQL password
    database="linguify"
)
cursor = conn.cursor()

# List of quiz questions
questions = [
    {
        "question": "¿Qué hiciste el fin de semana pasado?",
        "options": {
            "a": "Fui al cine con mis amigos.",
            "b": "Comía en casa todos los días.",
            "c": "Estoy estudiando para un examen.",
            "d": "Iré de compras mañana."
        },
        "correct": "a"
    },
    {
        "question": "¿Cuándo empieza la clase de español?",
        "options": {
            "a": "Empezó ayer.",
            "b": "Empieza a las dos de la tarde.",
            "c": "Termina a las cinco.",
            "d": "Estoy en casa ahora."
        },
        "correct": "b"
    },
    {
        "question": "¿Qué necesitas para cocinar una tortilla?",
        "options": {
            "a": "Un libro y una revista.",
            "b": "Huevos y aceite.",
            "c": "Un bolígrafo y un cuaderno.",
            "d": "Una computadora."
        },
        "correct": "b"
    },
    {
        "question": "¿Dónde está el banco más cercano?",
        "options": {
            "a": "Está en la esquina de la calle.",
            "b": "Voy a ir al banco mañana.",
            "c": "Me gusta la comida española.",
            "d": "El banco es grande."
        },
        "correct": "a"
    },
    {
        "question": "¿Cómo estuvo la película que viste?",
        "options": {
            "a": "Estoy estudiando.",
            "b": "Estará interesante.",
            "c": "Fue muy aburrida.",
            "d": "Voy al cine después."
        },
        "correct": "c"
    }
]

# Global variables
current_question = 0
selected_option = None
score = 0
answer_checked = False

# Function to save the score to the database
def save_score_to_db(user_id, language_id, difficulty_level, score):
    insert_query = """
    INSERT INTO quiz_scores (user_id, language_id, difficulty_level, score)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (user_id, language_id, difficulty_level, score))
    conn.commit()

# Function to display the question and options
def display_question():
    global current_question, answer_checked
    answer_checked = False
    reset_button_colors()
    selected_option.set(None)

    # Load the current question and its options
    question_data = questions[current_question]
    question_label.config(text=question_data["question"])
    option_button1.config(text=question_data["options"]["a"], state="normal")
    option_button2.config(text=question_data["options"]["b"], state="normal")
    option_button3.config(text=question_data["options"]["c"], state="normal")
    option_button4.config(text=question_data["options"]["d"], state="normal")

    next_button.config(state="disabled")

# Function to reset button colors to default
def reset_button_colors():
    option_button1.config(bg="white")
    option_button2.config(bg="white")
    option_button3.config(bg="white")
    option_button4.config(bg="white")

# Function to highlight selected option in yellow
def select_option(option):
    reset_button_colors()
    selected_option.set(option)
    if option == "a":
        option_button1.config(bg="yellow")
    elif option == "b":
        option_button2.config(bg="yellow")
    elif option == "c":
        option_button3.config(bg="yellow")
    elif option == "d":
        option_button4.config(bg="yellow")

# Function to check the selected answer
def check_answer():
    global current_question, score, answer_checked

    if selected_option.get() is None or answer_checked:
        return

    correct_option = questions[current_question]["correct"]

    if selected_option.get() == correct_option:
        highlight_button_correct(correct_option)
        score += 1  # Increase score if correct
    else:
        highlight_button_wrong(correct_option, selected_option.get())

    answer_checked = True  # Mark that the answer has been checked
    next_button.config(state="normal")  # Enable the next button after confirming the answer

# Function to highlight the correct answer (green) and wrong answer (red)
def highlight_button_correct(correct_option):
    if correct_option == "a":
        option_button1.config(bg="green")
    elif correct_option == "b":
        option_button2.config(bg="green")
    elif correct_option == "c":
        option_button3.config(bg="green")
    elif correct_option == "d":
        option_button4.config(bg="green")

def highlight_button_wrong(correct_option, selected_option):
    highlight_button_correct(correct_option)

    if selected_option == "a":
        option_button1.config(bg="red")
    elif selected_option == "b":
        option_button2.config(bg="red")
    elif selected_option == "c":
        option_button3.config(bg="red")
    elif selected_option == "d":
        option_button4.config(bg="red")

# Function to go to the next question
def next_question():
    global current_question

    if current_question < len(questions) - 1:
        current_question += 1
        display_question()
    else:
        show_result()

# Function to show the result in a popup
def show_result():
    global score
    user_id = 1  # Assuming you have user_id fetched from your login system
    language_id = 5  # Spanish Intermediate
    difficulty_level = 'intermediate'

    save_score_to_db(user_id, language_id, difficulty_level, score)

    if score == 5:
        show_score_popup("show_scorefive.png")
    elif score == 4:
        show_score_popup("show_scorefour.png")
    elif score == 3:
        show_score_popup("show_scorethree.png")
    elif score == 2:
        show_score_popup("show_scoretwo.png")
    elif score == 1:
        show_score_popup("show_scoreone.png")
    else:
        show_score_popup("show_scorezero.png")

def show_score_popup(image_path):
    result_window = tk.Toplevel(window)
    result_window.title("High Score")
    result_window.geometry("900x220")

    highscore_bg_img = ImageTk.PhotoImage(Image.open(f"./images/quiz_score/{image_path}"))
    background_label = Label(result_window, image=highscore_bg_img)
    background_label.place(relx=0, rely=0, width=900, height=220)
    background_label.image = highscore_bg_img  # Keep a reference to avoid garbage collection

    # Start Learning button
    start_learning_image = ImageTk.PhotoImage(Image.open("./images/start_learning.png"))
    start_learning_button = Button(result_window, image=start_learning_image, command=lambda: [open_learning_page(), result_window.destroy(),window.destroy()])
    start_learning_button.image = start_learning_image  # Keep a reference
    start_learning_button.place(x=315, y=152)

def open_learning_page():
    os.system("python session_esp_inter.py")  # Replace with your actual learning page script

# Set up the Tkinter window
window = tk.Tk()
window.title("Quick Quiz")
window.geometry("1366x768")

img_bg = Image.open("./images/quiz_inter_adv.png")
bg_image = ImageTk.PhotoImage(img_bg)
background_label = tk.Label(window, image=bg_image)
background_label.place(relx=0, rely=0, width=1366, height=768)

# Main Question Box
question_label = tk.Label(window, text="", font=("Arial", 40), bg="white", width=32)
question_label.place(x=170, y=172)

# Option buttons (4 options)
selected_option = tk.StringVar()

option_button1 = tk.Button(window, text="", font=("Helvetica", 25), width=25, height=2, bg="white", borderwidth=3, wraplength=400, cursor="hand2", command=lambda: select_option("a"))
option_button1.place(x=113, y=311)

option_button2 = tk.Button(window, text="", font=("Helvetica", 25), width=25, height=2, bg="white", borderwidth=3, wraplength=400, cursor="hand2", command=lambda: select_option("b"))
option_button2.place(x=768, y=311)

option_button3 = tk.Button(window, text="", font=("Helvetica", 25), width=25, height=2, bg="white", borderwidth=3, wraplength=400, cursor="hand2", command=lambda: select_option("c"))
option_button3.place(x=113, y=519)

option_button4 = tk.Button(window, text="", font=("Helvetica", 25), width=25, height=2, bg="white", borderwidth=3, wraplength=400, cursor="hand2", command=lambda: select_option("d"))
option_button4.place(x=768, y=519)

# Load images for Confirm and Next buttons
confirm_img = ImageTk.PhotoImage(Image.open("./images/confirm_button.png"))
next_img = ImageTk.PhotoImage(Image.open("./images/next_button.png"))

# Confirm button with image
confirm_button = tk.Button(window, image=confirm_img, cursor="hand2", command=check_answer)
confirm_button.place(x=558, y=670)

# Next button with image
next_button = tk.Button(window, image=next_img, cursor="hand2", command=next_question)
next_button.place(x=870, y=670)

logout_image = PhotoImage(file="./images/logout_button.png")
logout_button = Button(window, image=logout_image, borderwidth=0, command=lambda: logout(window, conn))
logout_button.image = logout_image
logout_button.place(x=1185, y=705)

def logout(level_selection_window, conn):
    messagebox.showinfo("Logout", "You have been logged out.")
    level_selection_window.destroy()
    os.system("python login_page.py")

# Start the quiz by displaying the first question
display_question()

# Start the Tkinter main loop
window.mainloop()