import tkinter as tk
from tkinter import Button, Label, PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
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


# List of quiz questions in French
questions = [
    {
        "question": "Que faisais-tu le week-end dernier ?", #(What did you do last weekend?)
        "options": {
            "a": "Je suis allé au cinéma avec mes amis.",   #(I went to the movies with my friends.)
            "b": "Je mangeais à la maison tous les jours.",  #(I ate at home every day.)
            "c": "J'étudie pour un examen.",  #(I am studying for an exam.)
            "d": "J'irai faire du shopping demain."  #(I will go shopping tomorrow.)
        },
        "correct": "a"
    },
    {
        "question": "Quand commence le cours de français ?", #(When does the French class start?)
        "options": {
            "a": "Il a commencé hier.",  #(It started yesterday.)
            "b": "Il commence à deux heures de l'après-midi.",  #(It starts at 2 p.m.)
            "c": "Il se termine à cinq heures.",  #(It ends at 5.)
            "d": "Je suis à la maison maintenant."  #(I am at home now.)
        },
        "correct": "b"
    },
    {
        "question": "Que faut-il pour cuisiner une omelette ?", #(What do you need to cook an omelette?)
        "options": {
            "a": "Un livre et un magazine.",  #(A book and a magazine.)
            "b": "Des œufs et de l'huile.",  #(Eggs and oil.)
            "c": "Un stylo et un cahier.",  #(A pen and a notebook.)
            "d": "Un ordinateur."  #(A computer.)
        },
        "correct": "b"
    },
    {
        "question": "Où se trouve la banque la plus proche ?", #(Where is the nearest bank?)
        "options": {
            "a": "Elle est au coin de la rue.",  #(It’s on the corner of the street.)
            "b": "Je vais aller à la banque demain.",  #(I’m going to the bank tomorrow.)
            "c": "J'aime la cuisine française.",  #(I like French food.)
            "d": "La banque est grande."  #(The bank is big.)
        },
        "correct": "a"
    },
    {
        "question": "Comment était le film que tu as vu ?", #(How was the movie you watched?)
        "options": {
            "a": "C'était très ennuyeux.",  #(It was very boring.)
            "b": "Ce sera intéressant.",  #(It will be interesting.)
            "c": "C'était très passionnant.",  #(It was very exciting.)
            "d": "Je vais au cinéma plus tard."  #(I’m going to the movies later.)
        },
        "correct": "a"
    }
]


# Global variables
current_question = 0
selected_option = None
score = 0
answer_checked = False  # This will track whether the user has already confirmed the answer

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
    answer_checked = False  # Reset answer check status for the new question
    reset_button_colors()  # Reset button colors
    selected_option.set(None)  # Reset selected option

    # Load the current question and its options
    question_data = questions[current_question]
    question_label.config(text=question_data["question"])
    option_button1.config(text=question_data["options"]["a"], state="normal")
    option_button2.config(text=question_data["options"]["b"], state="normal")
    option_button3.config(text=question_data["options"]["c"], state="normal")
    option_button4.config(text=question_data["options"]["d"], state="normal")

    next_button.config(state="disabled")  # Disable the next button until answer is confirmed

# Function to reset button colors to default
def reset_button_colors():
    option_button1.config(bg="white")
    option_button2.config(bg="white")
    option_button3.config(bg="white")
    option_button4.config(bg="white")

# Function to highlight selected option in yellow
def select_option(option):
    reset_button_colors()  # Reset all buttons to white
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
        return  # Do nothing if no option is selected or answer already checked

    correct_option = questions[current_question]["correct"]

    # Check if the selected option is correct
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
        show_result()  # Show the result popup at the end of the quiz

# Function to show the result in a popup
def show_result():
    global score
    user_id = 1  # Assuming you have user_id fetched from your login system
    language_id = 8  # Spanish Intermediate (you might need to change this dynamically)
    difficulty_level = 'intermediate'

    # Save the score to the database
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
    os.system("python session_fr_inter.py")

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
confirm_img = ImageTk.PhotoImage(Image.open("./images/confirm_button.png"))  # Replace with your actual image path
next_img = ImageTk.PhotoImage(Image.open("./images/next_button.png"))  # Replace with your actual image path

# Confirm button with image
confirm_button = tk.Button(window, image=confirm_img, cursor="hand2", command=check_answer)
confirm_button.place(x=558, y=670)

# Next button with image
next_button = tk.Button(window, image=next_img,  cursor="hand2", command=next_question)
next_button.place(x=870, y=670)

logout_image = PhotoImage(file="./images/logout_button.png")  # Provide the path to your logout button image
logout_button = Button(window, image=logout_image, borderwidth=0,
                                   command=lambda: logout(window, conn))
logout_button.image = logout_image  # Keep a reference to avoid garbage collection
logout_button.place(x=1185, y=705)  # Adjust position based on your layout

def logout(level_selection_window, conn):
    """Logout function that closes the language selection window and returns to login."""
    messagebox.showinfo("Logout", "You have been logged out.")
    level_selection_window.destroy()  # Close the language selection window
    os.system("python login_page.py")
    level_selection_window.deiconify()

# Start the quiz by displaying the first question
display_question()

# Start the Tkinter main loop
window.mainloop()