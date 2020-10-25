from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")

lbl = Label(window, text="Hello", font=("Arial Bold", 50))

lbl.grid(column=0, row=0)
window.geometry('800x600')
window.mainloop()