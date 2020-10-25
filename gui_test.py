import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk

# --- functions ---

def popup_window():
    window = tk.Toplevel()

    label = tk.Label(window, text="Hello World!")
    label.pack(fill='x', padx=50, pady=5)

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')

def popup_showinfo():
    showinfo("ShowInfo", "Hello World!")

def onChangeCombobox(event):
    print(comboExample.current(), comboExample.get())
# --- main ---

root = tk.Tk()
root.geometry('800x600')

button_bonus = tk.Button(root, text="Window", command=popup_window)
button_bonus.grid()

button_showinfo = tk.Button(root, text="ShowInfo", command=popup_showinfo)
button_showinfo.grid()

button_close = tk.Button(root, text="Close", command=root.destroy)
button_close.grid()

comboExample = ttk.Combobox(root,
                            values=[
                                    "January",
                                    "February",
                                    "March",
                                    "April"],
                            state="readonly")

comboExample.grid()
comboExample.current(1)

comboExample.bind("<<ComboboxSelected>>", onChangeCombobox)
print(comboExample.current(), comboExample.get())

root.mainloop()