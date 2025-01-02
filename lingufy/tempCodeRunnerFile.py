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
    start_learning_button = Button(result_window, image=start_learning_image, command=lambda: [open_learning_page(), result_window.destroy()])
    start_learning_button.image = start_learning_image  # Keep a reference
    start_learning_button.place(x=315, y=152)
