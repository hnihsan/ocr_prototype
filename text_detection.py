import cv2
import pytesseract
from Tools import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image
from PIL import ImageTk
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def start_ocr():
    print("Accessing device's camera...")
    result = ""
    ok_flag = True

    while ok_flag:
        ok_flag, frame = cap.read()
        # filtered = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filtered = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # ret, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        boxes = pytesseract.image_to_data(filtered, config='-c preserve_interword_spaces=2')

        for a, b in enumerate(boxes.splitlines()):
            # print(b)
            if a!=0:
                b = b.split()
                if len(b)==12:
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    cv2.putText(filtered,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
                    cv2.rectangle(filtered, (x,y), (x+w, y+h), (50, 50, 255), 2)
                    result = FilterAlphanumeric(b[11])

        img = ResizeWithAspectRatio(filtered, height=600)
        show_frame = cv2.imshow('Scanning Item ..', img)

        print("Output: " + result + "| "+str(len(result)))

        if not ok_flag:
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) == 27:
            ok_flag = False
            cv2.destroyAllWindows()
            break

        if len(result) >= 5 and len(result) <=10:
            print("Gotcha")
            cv2.imwrite('scanned_item.png', filtered)
            cv2.destroyAllWindows()

            break
        cv2.waitKey(1)

    return result

def update_image(image_panel, image_url):
    img = cv2.imread(image_url)
    img = ResizeWithAspectRatio(img, height=300)
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    image_panel.configure(image=imgtk)
    image_panel.image = imgtk

def popup_window(status_text, scanned_item):
    window = tk.Toplevel()

    label = tk.Label(window, text="Barang Berhasil "+status_text, font=("Helvetica",20), pady=5)
    label.grid()

    image_panel = tk.Label(window)
    image_panel.grid()
    update_image(image_panel, 'scanned_item.png')

    label = tk.Label(window, text='Serial Number Terbaca:', font=("Helvetica", 10), pady=3)
    label.grid()

    label = tk.Label(window, text=scanned_item, font=("Courier",20), pady=3)
    label.grid()

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.grid()

def btn_pinjam_action():
    scanned_item = start_ocr()
    if len(scanned_item) >= 5 and len(scanned_item) <=10:
        popup_window('Dipinjam', scanned_item)

def btn_retur_action():
    scanned_item = start_ocr()
    if len(scanned_item) >= 5 and len(scanned_item) <=10:
        popup_window('Dikembalikan', scanned_item)

def onChangeCombobox(event):
    global cap, comboExample
    cap = cv2.VideoCapture(comboExample.current())

def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1

    print(arr)
    if len(arr) > 1:
        return arr[1]
    else:
        return arr[0]

cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Serial Number Scanner")
root.geometry('400x300')
root.resizable(False, False)

sub_header = tk.Label(root, text="OCR System Prototype:", font=("Helvetica",12))
sub_header.pack(fill='x')

header = tk.Label(root, text="Serial Number Scanner", font=("Helvetica",18))
header.pack(fill='x', pady=10)

choose_src_label = tk.Label(root, text="Select video cam source:", font=("Helvetica",10))
choose_src_label.pack(fill='x')

comboExample = ttk.Combobox(root,
                            values=[
                                    "Webcam",
                                    "USB Camera Device",],
                            state="readonly")

comboExample.pack( )
comboExample.current(0)
comboExample.bind("<<ComboboxSelected>>", onChangeCombobox)

btn_pinjam = tk.Button(root, text="Pinjam", command=btn_pinjam_action, width=30, height=8, padx=5, pady=5)
btn_pinjam.pack(side=LEFT, anchor=S, )

btn_retur = tk.Button(root, text="Kembalikan", command=btn_retur_action, width=30, height=8, padx=5, pady=5)
btn_retur.pack(side=RIGHT, anchor=S)


root.mainloop()
# Tutorial
# img = cv2.imread('radiation.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
# print(pytesseract.image_to_string(img))
# img = ResizeWithAspectRatio(img, width=720)
# cv2.imshow('img', img)
#
# cv2.waitKey(0)
#
