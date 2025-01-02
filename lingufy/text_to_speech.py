from tkinter import *
import pyttsx3
root =Tk()
root.title("Linguify")
root.geometry("800x500")
root.iconbitmap('D:\Linguify')
engine=pyttsx3.init()
engine.say("Welcome to linguify Here we provide one stop solution to all the language learning")
engine.runAndWait()