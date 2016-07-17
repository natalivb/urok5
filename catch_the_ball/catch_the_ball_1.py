from tkinter import *
 

def init_main_window():
    global root, canvas, lab4,  scores, but, but1

    root = Tk()
    root.title("Поймай мяч")
    root["bg"] = "#a8f192"
    fra1 = Frame(root,width=400,height=150,bg="#a8f192")
    but = Button(fra1,text="начать игру",   
                  width=15, height=1,
                  font="Arial 10",
                  bg="#fdf63e") 
    but1 = Button(fra1,text="очистить холст",   
                  width=15, height=1,
                  font="Arial 10",
                  bg="#fdf63e")
    
    lab = Label(fra1,text="минимальный радиус шарика от  10  до 20: ",
                font="Arial 10", bg="#a8f192")
    ent = Entry(fra1,width=20,bd=3,bg="lightyellow")
     
    lab1 = Label(fra1,text="максимальный  радиус шарика от 20 до 40: ",
                 font="Arial 10", bg="#a8f192")
    ent1 = Entry(fra1,width=20,bd=3,bg="lightyellow")
    

    lab.grid(row=0,column=0,columnspan=3)
    ent.grid(row=0,column=4)
    lab1.grid(row=1,column=0, columnspan=3)
    ent1.grid(row=1,column=4)
    but.grid(row=2,column=4)
    but1.grid(row=3,column=4)
    lab3 = Label(fra1,text="Ваши баллы: ", font="Arial 18", bg="#a8f192")
    lab3.grid(row=5,column=0,columnspan=1)
    lab4 = Label(fra1, text=scores, font="Arial 18", bg="#a8f192")
    lab4.grid(row=5,column=2,columnspan=1)

    fra2 = Frame(root,width=400,height=110,bg="#ccf6e4")
    fra1.pack()
    fra2.pack()
    
    canvas = Canvas(fra2,width=400,height=400,bg="#ccf6e4")
    canvas.bind("<Button>", click_ball)
    canvas.bind("<Motion>", move_all_balls)
    canvas.pack()


from random import choice, randint

ball_initial_number = 20
ball_minimal_radius = 15
ball_maximal_radius = 30
ball_available_colors = ['#836af1', '#c66af1', '#6aadf1', '#ecf16a', '#ec136a', '#1cf911']

def click_ball(event):
    global scores
    """ Обработчик событий мышки для игрового холста canvas
    :param event: событие с координатами клика
    По клику мышкой нужно удалять тот объект, на который мышка указывает.
    А также засчитываеть его в очки пользователя.
    """
    obj = canvas.find_closest(event.x, event.y)
    x1, y1, x2, y2 = canvas.coords(obj)

    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        canvas.delete(obj)
        scores += 1
        lab4['text']=scores
        # считаем баллы по удаленному объекту
        create_random_ball()

def click_but1(event):
    """ очищает холст
    """
    canvas.delete('all')
    lab4['text']=0
def move_all_balls(event):
    """ передвигает все шарики на чуть-чуть
    """
    for obj in canvas.find_all():
        dx = randint(-3, 3)
        dy = randint(-3, 3)
        canvas.move(obj, dx, dy)

def create_random_ball():
    """
    создаёт шарик в случайном месте игрового холста canvas,
     при этом шарик не выходит за границы холста!
    """
    R = randint(ball_minimal_radius, ball_maximal_radius)
    x = randint(0, int(canvas['width'])-1-2*R)
    y = randint(0, int(canvas['height'])-1-2*R)
    canvas.create_oval(x, y, x+2*R, y+2*R, width=1, fill=random_color())


def random_color():
    """
    :return: Случайный цвет из некоторого набора цветов
    """
    return choice(ball_available_colors)


def init_ball_catch_game(event):
    """
    Создаём необходимое для игры количество шариков, по которым нужно будет кликать.
    """
    for i in range(ball_initial_number):
        create_random_ball()



scores = 0
if __name__ == "__main__":
    init_main_window()
    
    but.bind('<Button-1>', init_ball_catch_game)
    but1.bind('<Button-1>', click_but1)

root.mainloop() 
