import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from gtts import gTTS
import io
import pygame

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Function to fetch questions from the database
def get_questions(language_id, session_number, db, cur):
    cur.execute("SELECT question_id, question_text, option_1, option_2, option_3, option_4, correct_option FROM questions WHERE language_id = %s AND session_number = %s", 
                (language_id, session_number))
    return cur.fetchall()

# Function to check the selected answer and update button colors
def check_answer(selected_option, correct_option, buttons, results):
    # Disable all buttons after submission
    for button in buttons:
        button.config(state=DISABLED)

    # Reset all buttons to default colors first
    for button in buttons:
        button.config(bg="white", fg="black")  # Reset background to white and text color to black

    if selected_option == correct_option:
        buttons[correct_option - 1].config(bg="green")  # Change correct button to green
        results['correct'] += 1  # Increment correct answers count
    else:
        buttons[correct_option - 1].config(bg="green")  # Change correct button to green
        results['incorrect'] += 1  # Increment incorrect answers count

    # Reset the button text color back to black
    for button in buttons:
        button.config(fg="black")  # Set text color to black

# Function to display each question
def display_question(window, question_data, question_index, total_questions, language_id, session_number, db, cur, img_bg, results):
    if question_index >= total_questions:
        show_results(window, language_id, session_number, results)  # Show the results after the last question
        return
    
    question = question_data[question_index]
    question_id, question_text, option_1, option_2, option_3, option_4, correct_option = question

    # Clear the window
    for widget in window.winfo_children():
        widget.destroy()

    # Add background image
    background_label = Label(window)
    background_label.place(relx=0, rely=0, width=1366, height=768)
    background_label.configure(image=img_bg)

    # Load play button image for both the question and options
    play_img = ImageTk.PhotoImage(Image.open("./images/playbutton.png").resize((60, 60), Image.Resampling.LANCZOS))

    # Display question text and a button to play the question via TTS
    question_label = Label(window, text=question_text, font=("Helvetica", 40), bg="white", cursor="hand2", width=32, wraplength=1000)
    question_label.place(relx=0.5, rely=0.1, anchor="center")
    
    play_question_button = Button(window, image=play_img, command=lambda: play_tts(question_text, 'en'), bg="white", borderwidth=0)
    play_question_button.place(x=1251, y=109)

    selected_option = IntVar()
    buttons = []

    # Create and place option buttons (1 and 2 in the same row, 3 and 4 in the row below)
    options = [(option_1, 130, 295), (option_2, 790, 295), (option_3, 130, 505), (option_4, 790, 505)]
    
    for i, (option, x_pos, y_pos) in enumerate(options, start=1):
        option_button = Button(window, text=option, bg="white", fg="black", cursor="hand2", font=("Helvetica", 35), width=15, height=2, borderwidth=3, wraplength=400, command=lambda opt=i: select_option(opt, buttons))
        option_button.place(x=x_pos, y=y_pos)
        buttons.append(option_button)
        play_option_button = Button(window, image=play_img, bg="white", borderwidth=0, command=lambda opt=option: play_tts(opt, 'es'))
        play_option_button.place(x=x_pos + 450, y=y_pos + 40)

    # Load images for Submit and Next buttons
    confirm_img = ImageTk.PhotoImage(Image.open("./images/confirm_button.png"))
    next_img = ImageTk.PhotoImage(Image.open("./images/next_button.png"))

    # Submit button to check answer
    submit_button = Button(window, image=confirm_img, cursor="hand2", 
                           command=lambda: check_answer(selected_option.get(), correct_option, buttons, results))
    submit_button.place(x=558, y=670)
    
    # Next Question button (will be used after checking answer)
    next_question_button = Button(window, image=next_img, cursor="hand2",
                                  command=lambda: display_question(window, question_data, question_index + 1, total_questions, language_id, session_number, db, cur, img_bg, results))
    next_question_button.place(x=870, y=670)

    # Keep a reference to the images to prevent them from being garbage collected
    window.confirm_img = confirm_img
    window.next_img = next_img
    window.play_img = play_img

def select_option(option, buttons):
    # Change the selected button to yellow and reset others to white
    for idx, button in enumerate(buttons):
        if idx + 1 == option:
            button.config(bg="yellow")  # Change the selected button to yellow
        else:
            button.config(bg="white")  # Reset others to white

# Function to play text-to-speech for a given text
def play_tts(text, language='es'):
    tts = gTTS(text=text, lang=language)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    
    pygame.mixer.music.load(audio_fp, 'mp3')
    pygame.mixer.music.play()

# Function to show results and provide the next session button
def show_results(window, language_id, session_number, results):
    correct = results['correct']
    total = results['total']

    # Clear the window to show results
    for widget in window.winfo_children():
        widget.destroy()

    # Display the score
    result_label = Label(window, text=f"Session {session_number} Complete! You answered {correct} out of {total} questions correctly.", 
                         font=("Helvetica", 30), bg="white")
    result_label.place(relx=0.5, rely=0.4, anchor="center")

    # Load the next session button image
    next_session_img = ImageTk.PhotoImage(Image.open("./images/next_session_button.png"))

    if session_number < 7:  # If there are more sessions
        next_session_button = Button(window, image=next_session_img, cursor="hand2", 
                                     command=lambda: start_session(window, language_id, session_number + 1))
        next_session_button.place(x=550, y=500)
    else:  # If it's the last session
        message_label = Label(window, text="You have completed all sessions! Well done!", font=("Helvetica", 35), bg="white")
        message_label.place(relx=0.5, rely=0.6, anchor="center")

    # Keep a reference to the next session button image to prevent garbage collection
    window.next_session_img = next_session_img

# Main function to start the session
def start_session(window, language_id, session_number):
    window.geometry("1366x768")
    window.title(f"Session {session_number} - Language Learning")

    # Load the background image
    img_bg = PhotoImage(file="./images/session_page.png")  # Use your own background image path

    try:
        # Connect to the database
        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinayak@23",
            database="LINGUIFY"
        ) as db:
            cur = db.cursor()
            questions = get_questions(language_id, session_number, db, cur)
            total_questions = len(questions)

            # Initialize results dictionary
            results = {'correct': 0, 'incorrect': 0, 'total': total_questions}

            if total_questions > 0:
                display_question(window, questions, 0, total_questions, language_id, session_number, db, cur, img_bg, results)
            else:
                messagebox.showinfo("No Questions", "No questions available for this session.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Test the session with a sample username and session number
if __name__ == "__main__":
    root = Tk()
    language_id = 5  # Replace with actual language ID (e.g., 1 for English)
    session_number = 1  # Start from the first session
    start_session(root, language_id, session_number)
    root.mainloop()
