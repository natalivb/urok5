from tkinter import *
from random import *


def init_main_window():
    global root, canvas,lab4,ent, lab5, scores, a
    root = Tk()
    lab4 = Label(root, text=scores)
    lab4.pack()
    canvas = Canvas(root, background='#8ef4e9', width=400, height=400)
    canvas.pack()
    ent = Entry(root,width=20,bd=3,bg="lightyellow")   
    ent.pack()
   
    
    
    

  

def mouse_click(event):
    global scores, a
    scores += 1
    lab4['text']=scores     
    a = ent.get()
    a = int(a)
    canvas.create_oval(2+a*2, 2+a*2, scores*4+scores*5, scores*4+scores*5, width=2, fill='red')
   
scores = 0
a = 0

if __name__ == "__main__":
    init_main_window()
    
    canvas.bind('<Button-1>',mouse_click)
   
    root.mainloop()

 


