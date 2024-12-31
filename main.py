from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

def pressed_button():
    global flip_timer, random_word
    window.after_cancel(flip_timer)
    random_word = random.choice(file_data_dict)
    canvas.itemconfig(card_title, text= "French")
    canvas.itemconfig(card_word, text = random_word["French"])
    canvas.itemconfig(canvas_image, image=back)
    canvas.itemconfig(card_title, fill= "white")
    canvas.itemconfig(card_word, fill= "white")
    flip_timer = window.after(3000, flip_card_front)
    
def flip_card_front():
    canvas.itemconfig(canvas_image, image=front)
    canvas.itemconfig(card_title, text= "English")
    canvas.itemconfig(card_word, text = random_word["English"])
    canvas.itemconfig(card_title, fill= "black")
    canvas.itemconfig(card_word, fill= "black")
    window.after(3000, pressed_button)
    
def correct_answer():
    file_data_dict.remove(random_word)
    words_to_learn = pandas.DataFrame(file_data_dict)
    words_to_learn.to_csv(r"data/words_to_learn.csv", index=False)
    pressed_button()   

window = Tk()
window.title("Language Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card_front)

front = PhotoImage(file=r"images\card_front.png")
back = PhotoImage(file=r"images\card_back.png")
right = PhotoImage(file=r"images\right.png")
wrong = PhotoImage(file=r"images\wrong.png")

canvas = Canvas(width=600, height=326, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(300, 163, image=front)
card_title = canvas.create_text(300, 50, text="", font=("Arial", 30, "italic"))
card_word = canvas.create_text(300, 163, text="", font=("Arial", 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

correct_button = Button(image=right, highlightthickness=0,command=correct_answer)
correct_button.grid(column=0, row=1)

wrong_button = Button(image=wrong, highlightthickness=0, command=pressed_button)
wrong_button.grid(column=1, row=1)

correct_count = 0
wrong_count = 0

# Here I take the words that I have not reviewed yet (words_to_learn.csv)
# if the file does not exist I create it 
try:
    data = pandas.read_csv(r"data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(r"data/french_words.csv")
    file_data_dict = original_data.to_dict(orient="records")
# if the initial attempt to read the "words_to_learn.csv" was succesful this else block executes
else:
    file_data_dict = data.to_dict(orient="records")

pressed_button()

window.mainloop()
