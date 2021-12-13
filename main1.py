from tkinter import *
import pandas
from random import choice
word = {}

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 40, "bold")

# window setup
window = Tk()
window.title("Rob's Flash Card Application")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# GUI setup
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 268, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# images setup
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

# import words
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    vocabulary = data.to_dict(orient="records")

# if answer is wrong
def change_word():
    global word, vocabulary, flip_timer
    window.after_cancel(flip_timer)
    word = choice(vocabulary)
    canvas.itemconfig(title_card, text="French", fill="black")
    canvas.itemconfig(word_card, text=word["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    window.after(3000, card_flip)

# if answer is correct
def delete_word():
    global vocabulary, word
    vocabulary.remove(word)
    vocab_df = pandas.DataFrame(vocabulary, columns=["French", "English"])
    vocab_df.to_csv("data/words_to_learn.csv")
    change_word()



# text setup
title_card = canvas.create_text(400, 150, text="title", font=TITLE_FONT)
word_card = canvas.create_text(400, 263, text="word", font=WORD_FONT)

# buttons setup
true_button = Button(image=right, highlightthickness=0, command=delete_word)
false_button = Button(image=wrong, highlightthickness=0, command=change_word)
true_button.grid(row=1, column=0)
false_button.grid(row=1, column=1)

# card back
card_back = PhotoImage(file="images/card_back.png")

def card_flip():
    global word
    canvas.itemconfig(card_background, image=card_back)
    canvas.itemconfig(title_card, text="English", fill="white")
    canvas.itemconfig(word_card, text=word["English"], fill="white")

flip_timer = window.after(3000, card_flip)
change_word()

window.mainloop()
