from tkinter import *
from random import choice, randint

from tkinter.messagebox import *

frame_sleep_time = 50  # задержка между кадрами в милисекундах
dt = 0.15  # квант игрового времени между кадрами
g = 10    # гравитационная постоянная игры


def random_color():
    colors = ['#836af1', '#c66af1', '#6aadf1', '#ecf16a', '#ec136a', '#1cf911', '#f4a2c8']
    return choice(colors)

def random_color1():
    colors = ['#836a90', '#c66a90', '#6aad90', '#ecf190', '#ec1390', '#1cf990', '#f4a210']
    return choice(colors)

class Ball:
    def __init__(self):
        self.color = 'white'
        self.r = randint(20, 30)
        self.x, self.y = self.generate_random_ball_coord()
        self.vx, self.vy = self.generate_random_ball_velocity()
        
        self.avatar = canvas.create_oval(self.x - self.r, self.y - self.r,
                                         self.x + self.r, self.y + self.r, fill=random_color(), outline = random_color() )

        self.avatar1 = canvas.create_oval(self.x -10, self.y -10,
                                          self.x + self.r-4, self.y + self.r-4, outline = random_color(), fill=random_color1())


        self.avatar2 = canvas.create_oval(self.x -3, self.y -3,
                                         self.x + self.r-7, self.y + self.r-7, outline = 'white', fill=self.color)

    def move(self):
        new_x = self.x + 2*self.vx*dt
        new_y = self.y + 2*self.vy*dt + g*dt**2/2
        self.vy += g*dt
        if new_x < self.r or new_x > 400 - self.r:
            new_x = self.x  # rolling back coordinate!
            self.vx = -self.vx
        if new_y < self.r or new_y > 400 - self.r:
            new_y = self.y  # rolling back coordinate!
            self.vy = -self.vy
        canvas.move(self.avatar, new_x - self.x, new_y - self.y)
        canvas.move(self.avatar1, new_x - self.x, new_y - self.y)
        canvas.move(self.avatar2, new_x - self.x, new_y - self.y)
        self.x, self.y = new_x, new_y

    def flick(self):
        new_x, new_y = self.generate_random_ball_coord()
        self.vx, self.vy = self.generate_random_ball_velocity()
        canvas.move(self.avatar, new_x - self.x, new_y - self.y)
        canvas.move(self.avatar1, new_x - self.x, new_y - self.y)
        canvas.move(self.avatar2, new_x - self.x, new_y - self.y)
        self.x, self.y = new_x, new_y

    def generate_random_ball_coord(self):
        x = randint(self.r, 400 - self.r)
        y = randint(self.r, 400 - self.r)
        return x, y

    def generate_random_ball_velocity(self):
        vx = randint(-10, +10)
        vy = randint(-10, +10)
        return vx, vy

    def check_collision(self, x, y):
        return (x - self.x)**2 + (y - self.y)**2 <= self.r**2



class Bullet(Ball):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.r = 10
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        canvas.coords(self.avatar, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        # FIXME: fill="black"
        


class Gun:
    """
    создание пушки в нижнем левом углу холста
    """
    def __init__(self):
        self.x = 0
        self.y = 400
        self.lx = 50
        self.ly = 50
        self.avatar = canvas.create_line(self.x, self.y, self.x + self.lx,
                                         self.y - self.ly, fill="blue", width=8)     

    def shoot(self):
        
        vx = self.lx
        vy = self.ly
        return Bullet(self.x + self.lx, self.y + self.ly, vx, vy)

    def aim(self, x, y):
        l = ((x - self.x)**2 + (y - self.y)**2)**0.5
        self.lx = 50*(x - self.x)/l
        self.ly = 50*(y - self.y)/l
        canvas.coords(self.avatar, self.x, self.y, self.x + self.lx, self.y + self.ly)

def time_event():
    global scores, label2

    # даём возможность подвинуться всем целям
    for target in targets:
        target.move()
    # если снаряд существует, то он летит
    if bullet:   # FIXME сделать много снарядов
        bullet.move()
        # проверка, не столкнулся ли снаряд с целью
        for target in targets:
            if target.check_collision(bullet.x, bullet.y):
                target.flick()
                scores += 1
                label2['text']=scores
                
    canvas.after(frame_sleep_time, time_event)

    
def mouse_move(event):
    # отслеживание курсора
    global gun
    gun.aim(event.x, event.y)

def mouse_click(event):
    global bullet
    if bullet:
        canvas.delete(bullet.avatar)
    bullet = gun.shoot()
    





def init_game():
    """
    начало игры
    """
    global gun
    gun = Gun()
    canvas.bind("<Motion>", mouse_move)
    
    
def init_main_window():
    global root, canvas, label2
    root = Tk()

    root["bg"] = "#a8f192"
    label1 = Label(root, text="Количество пораженных мишеней:", font="Arial 12")
    label1["bg"] = "#a8f192"
    label1.pack()
    label2 = Label(root, text="0", font="Arial 12")
    label2["bg"] = "#a8f192"
    label2.pack()
    canvas = Canvas(root,width=400,height=400,bg="#ccf6e4")
    canvas.config(cursor='hand2')
    canvas.pack()
    

scores = 0
if __name__ == "__main__":
    init_main_window()
    bullet = None
    init_game()
    canvas.bind("<Motion>", mouse_move)
    canvas.bind('<Button-1>', mouse_click)
    targets = [Ball() for i in range(10)]
    bullet = None
    time_event()  # начинаю циклически запускать таймер
root.mainloop() 

