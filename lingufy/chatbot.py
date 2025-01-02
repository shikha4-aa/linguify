import tkinter as tk
from tkinter import messagebox, Scrollbar, Frame, END

class LanguageLearningChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Lingufiy - Language Learning Assistant")
        self.root.geometry("500x500")  # Adjusted height for better usability
        
        # Create a frame for the chat history and scrollbar
        self.chat_frame = Frame(root)
        self.chat_frame.pack(pady=10)

        self.chat_history = tk.Text(self.chat_frame, height=20, width=60, state='disabled', wrap='word', bg="#f0f0f0", font=("Arial", 12))
        self.chat_history.pack(side=tk.LEFT)

        self.scrollbar = Scrollbar(self.chat_frame, command=self.chat_history.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        # User input frame
        self.input_frame = Frame(root)
        self.input_frame.pack(pady=10)

        self.user_input = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, padx=5)
        self.user_input.bind("<Return>", self.process_input)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.process_input)
        self.send_button.pack(side=tk.LEFT)

        self.bot_reply("Hello! Welcome to Lingufiy. I am your personal assistant.")
        self.language_selected = False
        self.language = None
        self.question_loop = False

    def bot_reply(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(END, "Bot: " + message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(END)

    def user_reply(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(END, "You: " + message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(END)

    def process_input(self, event=None):
        user_message = self.user_input.get()
        if user_message:
            self.user_reply(user_message)
            self.user_input.delete(0, tk.END)
            if not self.language_selected:
                self.select_language(user_message)
            elif self.language_selected and not self.question_loop:
                self.ask_reasons_for_learning(user_message)
            elif self.question_loop:
                self.handle_questions(user_message)

    def select_language(self, message):
        if message.lower() in ["hi", "hello"]:
            self.bot_reply("Which language do you want to learn? Choose from: English, French, Spanish.")
        elif message.lower() in ["english", "french", "spanish"]:
            self.language = message.lower()
            self.language_selected = True
            self.bot_reply(f"That's great! You want to learn {message.capitalize()}. Why do you want to learn this language?")
            self.bot_reply("Options: 1. Travel, 2. Career, 3. Culture, 4. Personal Interest")
        else:
            self.bot_reply("Sorry, I didn't understand that. Please choose from English, French, or Spanish.")

    def ask_reasons_for_learning(self, message):
        if message.lower() in ["1", "travel"]:
            self.bot_reply("Traveling is a great reason! Let's get started with your language lessons.")
        elif message.lower() in ["2", "career"]:
            self.bot_reply("That's great! Learning a language can definitely help in your career.")
        elif message.lower() in ["3", "culture"]:
            self.bot_reply("Exploring new cultures is a fantastic reason. Let's dive in!")
        elif message.lower() in ["4", "personal interest"]:
            self.bot_reply("Personal interest is a great motivator! Let's start learning.")
        else:
            self.bot_reply("Please choose one option: 1. Travel, 2. Career, 3. Culture, 4. Personal Interest.")
            return
        self.question_loop = True
        self.bot_reply("Do you have any questions about the language? (Type 'no' if you don't).")

    def handle_questions(self, message):
        if message.lower() == "no":
            self.bot_reply("Great! Let me know if you have any questions later.")
            self.question_loop = False  
        else:
            self.search_for_answer(message)

    def search_for_answer(self, question):
        # Dummy implementation; replace this with an actual search
        knowledge_base = {
            "how do you say hello in english": "In English, you say 'Hello!'",
            "how do you say goodbye in spanish": "In Spanish, you say 'Adiós!'",
            "how do you say thank you in french": "In French, you say 'Merci!'"
        }
        question = question.lower().strip()
        answer = knowledge_base.get(question)
        if answer:
            self.bot_reply(answer)
        else:
            self.bot_reply("Sorry, I am unable to answer this question right now. Please try again later.")

if __name__ == "__main__":  # Corrected main check
    root = tk.Tk()
    app = LanguageLearningChatbot(root)
    root.mainloop()