import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_pie_chart(scores):
    # Create a Tkinter window
    window = tk.Toplevel()
    window.title("Test Scores")

    # Pie chart data
    labels = ['Correct', 'Incorrect']
    sizes = [scores['correct'], scores['incorrect']]
    colors = ['blue', 'coral']
    explode = (0.1, 0)  # explode the 1st slice (Correct)

    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add the pie chart to the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    window.mainloop()

# Example usage
if __name__ == "__main__":
    scores = {'correct': 8, 'incorrect': 2}  # Example scores
    show_pie_chart(scores)
