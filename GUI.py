from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
from functions import detect_face, play_song, has_consecutive_repeats, open_spotify

global emotions
global stop_update
cap = cv2.VideoCapture(0)
emotions = []
stop_update = False

def read_frame():
    global stop_update
    if stop_update:
        return  
    else:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
    
    camera_label.after(10, read_frame)

def update_frame():
    global emotions, stop_update
    stop_update = True

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame, text = detect_face(frame)
        emotions.append(text)
        status, emotion = has_consecutive_repeats(emotions)
        if status and emotion!= None:
            open_spotify()
            time.sleep(3)
            play_song(emotion)
            emotions.clear()
            stop_update = False
            read_frame()
            return
        
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    
    camera_label.after(10, update_frame)

root = Tk()
root.geometry("1000x750")
root.title("Emotion Detector")
root.resizable(0, 0)

# Adding gradient background
gradient_frame = Canvas(root, width=1000, height=750)
gradient_frame.pack(fill='both', expand=True)

def draw_gradient(canvas, color1, color2):
    width = 1000
    height = 750
    limit = width
    (r1, g1, b1) = root.winfo_rgb(color1)
    (r2, g2, b2) = root.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        canvas.create_line(i, 0, i, height, fill=color, width=1)

draw_gradient(gradient_frame, "#3498db", "#2ecc71")

# Modern frame styling
MF = Frame(root, bd=8, bg="#3498db", relief=FLAT)
MF.place(x=0, y=0, height=50, width=1000)

menu_label = Label(MF, text="Emotion Detector", font=("Helvetica", 20, "bold"), bg="#3498db", fg="white", pady=0)
menu_label.pack(side=TOP, fill="x")

# Camera label
camera_label = Label(root, bg="#f0f0f0")
camera_label.place(relx=0.5, rely=0.1, anchor=N)

# Create a frame for buttons with modern styling
button_frame = Frame(root, bg="#f0f0f0")
button_frame.place(relx=0.5, rely=0.75, anchor=N)

# Modern button styling with rounded corners
class RoundedButton(Button):
    def __init__(self, master=None, **kw):
        Button.__init__(self, master=master, **kw)
        self.configure(
            width=15,
            height=2,
            relief=FLAT,
            bg="#2980b9",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0,
            font=("Helvetica", 14, "bold"),
            highlightthickness=0,
            padx=10,
            pady=10
        )

# "Detect Emotion" button
b2 = RoundedButton(button_frame, text='Detect Emotion', command=update_frame)
b2.grid(row=0, column=1, padx=10)

# Create a frame for displaying images
image_frame = Frame(root, bg="#f0f0f0")
image_frame.place(relx=0.5, rely=0.5, anchor=N)

# Modern image label styling
image_label_style = {
    "bg": "#f0f0f0",
    "bd": 0,
    "highlightthickness": 1,
    "highlightbackground": "#ccc"
}

read_frame()

root.mainloop()
