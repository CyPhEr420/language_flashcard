from tkinter import *
import pandas
from random import choice

language = input("Do you want to learn french or spanish:")


current_card = {}
to_learn = {}

try:
    data = pandas.read_csv(f"data/{language}_words_to_learn.csv")
except FileNotFoundError:
    orginal_data = pandas.read_csv(f"data/{language}_words.csv")
    to_learn = orginal_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

print(to_learn)


def get_words():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    french_word = current_card[language]
    canvas.itemconfig(lang, text=language)
    canvas.itemconfig(word, text=french_word)
    canvas.itemconfig(card_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    unlearned_words = pandas.DataFrame(to_learn)
    unlearned_words.to_csv(f"data/{language}_words_to_learn.csv", index=False)
    get_words()


def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(lang, text="English")
    canvas.itemconfig(word, text=current_card["english"])


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=600)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
lang = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_sign = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_sign, highlightthickness=0, command=get_words)
wrong_btn.grid(row=1, column=0)

right_sign = PhotoImage(file="images/right.png")
right_btn = Button(image=right_sign, highlightthickness=0, command=is_known)
right_btn.grid(row=1, column=1)

get_words()

window.mainloop()
