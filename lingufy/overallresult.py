import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import random

# Function to fetch user data from the database
def fetch_user_data(username):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinayak@23",
            database="LINGUIFY"
        )
        cur = db.cursor()
        query = "SELECT completed_lessons, total_lessons, badges, streak, correct_answers, incorrect_answers FROM users WHERE username = %s"
        cur.execute(query, (username,))
        result = cur.fetchone()

        if result:
            user_data['completed_lessons'], user_data['total_lessons'], badges, user_data['streak'], user_data['correct_answers'], user_data['incorrect_answers'] = result
            user_data['badges'] = badges.split(',') if badges else []

        db.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to update user data in the database
def update_user_data(username):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinayak@23",
            database="LINGUIFY"
        )
        cur = db.cursor()
        badges_str = ','.join(user_data['badges'])
        query = """
        UPDATE users 
        SET completed_lessons = %s, correct_answers = %s, incorrect_answers = %s, badges = %s, streak = %s
        WHERE username = %s
        """
        cur.execute(query, (user_data['completed_lessons'], user_data['correct_answers'], user_data['incorrect_answers'], badges_str, user_data['streak'], username))
        db.commit()
        db.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to update the progress bar and other user data
def update_progress():
    # Calculate progress percentage
    progress_percentage = (user_data['completed_lessons'] / user_data['total_lessons']) * 100
    progress_bar['value'] = progress_percentage
    percentage_label.config(text=f"Completion: {progress_percentage:.1f}%")

    # Update badge system
    if user_data['completed_lessons'] >= 10 and "Completion Badge" not in user_data['badges']:
        user_data['badges'].append("Completion Badge")
        messagebox.showinfo("Congratulations!", "You've earned the Completion Badge!")
    
    # Update streak tracker
    streak_label.config(text=f"Current Streak: {user_data['streak']} days")
    
    # Update performance summary
    summary_text.set(f"Correct Answers: {user_data['correct_answers']}\n"
                     f"Incorrect Answers: {user_data['incorrect_answers']}\n"
                     f"Badges: {', '.join(user_data['badges']) if user_data['badges'] else 'None'}")

    # Save progress to the database
    update_user_data(username)

# Function to simulate progress (completing a lesson)
def simulate_progress():
    # Simulate completing a lesson and answering correctly
    user_data['completed_lessons'] += 1
    user_data['correct_answers'] += random.randint(1, 5)  # Simulate correct answers
    user_data['incorrect_answers'] += random.randint(0, 2)  # Simulate incorrect answers
    update_progress()

# Sample user data (to be fetched from the database)
user_data = {
    'completed_lessons': 0,
    'total_lessons': 10,
    'badges': [],
    'streak': 0,
    'correct_answers': 0,
    'incorrect_answers': 0
}

# Create main Tkinter window
window = tk.Tk()
window.title("Language Learning App - User Progress Tracker")

# Create progress bar
progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
progress_bar.pack(pady=20)

# Label to show progress percentage
percentage_label = tk.Label(window, text="Completion: 0.0%")
percentage_label.pack(pady=5)

# Label for streak
streak_label = tk.Label(window, text=f"Current Streak: {user_data['streak']} days")
streak_label.pack(pady=5)

# Performance summary text variable
summary_text = tk.StringVar()
summary_label = tk.Label(window, textvariable=summary_text, justify='left')
summary_label.pack(pady=10)

# Simulate progress button
simulate_button = tk.Button(window, text="Complete Lesson", command=simulate_progress)
simulate_button.pack(pady=10)

# Fetch user data (replace 'username' with the actual logged-in username)
username = "User1"
fetch_user_data(username)

# Initial progress update
update_progress()

# Start the Tkinter main loop
window.mainloop()
