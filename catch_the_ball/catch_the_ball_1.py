from tkinter import *


def init_main_window():
    global root, canvas, lab4,  scores, to_start_the_game, to_clear_the_canvas, choose_the_radius, ent, ent1
    root = Tk()
    root.title("Поймай мяч")
    root["bg"] = "#a8f192"
    fra1 = Frame(root,width=400,height=150,bg="#a8f192")
    to_start_the_game = Button(fra1,text="начать игру",   
                            width=15, height=1,
                            font="Arial 10",
                            bg="#fdf63e") 
    to_clear_the_canvas = Button(fra1,text="очистить холст",   
                                  width=15, height=1,
                                  font="Arial 10",
                                  bg="#fdf63e")
    choose_the_radius = Button(fra1,text="ok",   
                  width=15, height=1,
                  font="Arial 10",
                  bg="#fdf63e")
    lab = Label(fra1,text="минимальный радиус шарика от  10  до 20: ",
                font="Arial 10", bg="#a8f192")
    ent = Entry(fra1, width=20, bd=3,bg="lightyellow")
     
    lab1 = Label(fra1,text="максимальный  радиус шарика от 20 до 40: ",
                 font="Arial 10", bg="#a8f192")
    ent1 = Entry(fra1, width=20,bd=3,bg="lightyellow")
    lab.grid(row=0,column=0,columnspan=3)
    ent.grid(row=0,column=4)
    lab1.grid(row=1,column=0, columnspan=3)
    ent1.grid(row=1,column=4)
    to_start_the_game.grid(row=3,column=4)
    to_clear_the_canvas.grid(row=3,column=1)
    choose_the_radius.grid(row=2,column=4)
    lab3 = Label(fra1,text="Ваши баллы: ", font="Arial 16", bg="#a8f192")
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
balls_coord = []#список координат шариков
balls_num = []#список номеров шариков

def enter_radius(event):
    """ осуществляется ввод радиусов шариков
    если введены некорректные значения радиусов,
    появляется окно с предупреждением об ошибке
    """
    global ent, ent1, ball_minimal_radius, ball_maximal_radius
    ball_minimal_radius = int(ent.get())
    ball_maximal_radius = int(ent1.get())
    if ball_minimal_radius < 10 or ball_minimal_radius > 20 or ball_maximal_radius < 20 or ball_maximal_radius > 40:
        input_error = Tk()
        
        input_error["bg"] = "red"
        lab4 = Label(input_error,text="Некорректное значение радиуса!",
                    font="Arial 10", bg="red")
        lab4.pack()
        
def click_to_clear_the_canvas(event):
    """ очищает холст
    """
    canvas.delete('all')
    lab4['text']=0

ball_available_colors = ['#836af1', '#c66af1', '#6aadf1', '#ecf16a', '#ec136a', '#1cf911']

def click_ball(event):
    """ Обработчик событий мышки для игрового холста canvas
    :param event: событие с координатами клика
    По клику мышкой нужно удалять тот объект, на который мышка указывает.
    А также засчитываеть его в очки пользователя.
    """
   
    global label, balls_coord, balls_num, scores
    obj = canvas.find_closest(event.x, event.y)
    num = obj[0]# вытаскиваем номер объекта из кортежа
    x1, y1, x2, y2 =canvas.coords(obj)
    if x1 < event.x < x2 and y1 < event.y < y2:
        index = balls_num.index(num)# определяем индекс элемента списка, где хранится номер объекта
        balls_num.pop(index)# удаляем элемент списка с номером объекта
        balls_coord.pop(index)# удаляем элемент списка с координатами объекта
        canvas.delete(obj)
        scores += 1
        lab4['text']=scores
        # считаем баллы по удаленному объекту
        create_random_ball()

  

def move_all_balls(event):#Передвигает все шарики
    global balls_coord
    for obj in balls_coord:
        x1, y1, x2, y2 =canvas.coords(obj[0])
        # проверяем, не выйдет ли шарик за границы холста
        if x1+obj[1]+obj[3]>=400 or x1+obj[1]<=0:
            obj[1]=-obj[1] #меняем направление движения
        if y1+obj[2]+obj[3]>=400 or y1+obj[2]<=0:
            obj[2]=-obj[2]
        canvas.move(obj[0],obj[1],obj[2])

def create_random_ball(): #Создание шарика в случайном месте игрового поля
    global balls_coord, balls_num, ball_minimal_radius, ball_maximal_radius
    R = randint(ball_minimal_radius, ball_maximal_radius)
    x = randint(R,int(canvas['width'])-R)
    y = randint(R,int(canvas['height'])-R)
    #рисуем шарик и запоминаем его номер в num_oval
    num_oval = canvas.create_oval(x, y, x+1.5*R, y+1.5*R, width=0, fill=random_color())
    dx = randint(-3, 3)
    dy = randint(-3, 3)
    # запоминаем идентификатор, вектор и радиус движения нового шарика
    balls_coord.append([num_oval, dx, dy, R])
    balls_num.append(num_oval)# запоминаем номер нового шарика

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
    
    to_start_the_game.bind('<Button-1>', init_ball_catch_game)
    to_clear_the_canvas.bind('<Button-1>', click_to_clear_the_canvas)
    choose_the_radius.bind('<Button-1>', enter_radius)
root.mainloop() 
