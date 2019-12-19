from tkinter import *
import matplotlib.pyplot as plt
import time
from statistics import mean
from EV import Evol
import random

def get_colour():
    nn = int(random.random()*0xFFFFFF)
    return "#"+(8-len(hex(nn)))*"0"+hex(nn)[2:]
    
my_random_colours =[get_colour() for i in range(1000)]
#print(random_colours)
def recup() :
    largeur = int(enter_1.get())
    hauteur = int(enter_2.get())
    nombre_de_creature = int(enter_3.get())
    A = Evol(nombre_de_creature,largeur,hauteur)
    B = display(A)
    B.launch()
    
class display :
    def __init__(self,class_in) :
        self.scale = float(enter_4.get())
        self.class_in = class_in
        self.Nod = int(enter_5.get())
        self.frame = float(enter_6.get())
        self.x = 1
        self.a = 1
        self.b = 1
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.ax2.set_ylim(0,3)
        self.ax3.set_ylim(0,2)
        self.ax4.set_ylim(0,2)
        self.factor = int(value_7.get())
    def launch(self) :
        if value_7.get()=="0" :
            for i in range(self.Nod) :
                self.class_in.move()
                while self.class_in.t < self.class_in.t_day-1 :
                    self.class_in.move()
                y = len(self.class_in.creatures)
                self.ax1.plot(self.x,y,"g^")
                speed_list = []
                size_list = []
                sence_list = []
                for i in self.class_in.creatures :
                    speed_list += [i.speed]
                    size_list += [i.hitbox]
                    sence_list += [i.sence]
                y2 = mean(speed_list)
                self.ax2.plot(self.x,y2,"b^")
                y3 = mean(size_list)
                self.ax3.plot(self.x,y3,"go")
                y4 = mean(sence_list)
                self.ax4.plot(self.x,y4,"bo")
                plt.pause(0.000005)
                self.x += 1
        else :
            window2 = Tk()
            canvas = Canvas(window2, width=(self.class_in.x-1)*100*self.scale,height = (self.class_in.y-1)*100*self.scale, background = "white")
            for i in self.class_in.creatures :
                canvas.create_oval((i.position[0]-0.5)*100*self.scale,(i.position[1]-0.5)*100*self.scale,(i.position[0]+0.5)*100*self.scale,(i.position[1]+0.5)*100*self.scale,fill = "#555555")
            canvas.create_text(200, 60, text="press s to start the simulation", font="Arial 16 italic", fill="black")
            canvas.pack()
            def clavier(event):
                touche = event.keysym
                if touche == "s":
                    for i in range(self.Nod) :
                        self.class_in.move()
                        while self.class_in.t < self.class_in.t_day-1 :
                            self.class_in.move()
                            if (self.class_in.day%self.factor) == 0 :
                                canvas.delete(ALL)
                                for index,i in enumerate(self.class_in.creatures) :
                                    canvas.create_oval( (i.position[0]-i.hitbox)*100*self.scale, (i.position[1]-i.hitbox)*100*self.scale, (i.position[0]+i.hitbox)*100*self.scale, (i.position[1]+i.hitbox)*100*self.scale,fill = my_random_colours[index])
                                for j in self.class_in.foods :
                                    canvas.create_oval( (j[0]-0.125)*100*self.scale, (j[1]-0.125)*100*self.scale, (j[0]+0.125)*100*self.scale, (j[1]+0.125)*100*self.scale,fill = "#005500")
                                time.sleep(self.frame)
                                canvas.create_text(100, 20, text="hour : {}, day : {}".format(self.class_in.t,self.class_in.day), font="Arial 16 italic", fill="black")
                                canvas.update()
                        y = len(self.class_in.creatures)
                        self.ax1.plot(self.x,y,"g^")
                        speed_list = []
                        size_list = []
                        sence_list = []
                        for i in self.class_in.creatures :
                            speed_list += [i.speed]
                            size_list += [i.hitbox]
                            sence_list += [i.sence]
                        y2 = mean(speed_list)
                        self.ax2.plot(self.x,y2,"b^")
                        y3 = mean(size_list)
                        self.ax3.plot(self.x,y3,"go")
                        y4 = mean(sence_list)
                        self.ax4.plot(self.x,y4,"bo")
                        plt.pause(0.000005)
                        self.x += 1
                    
                    
                    
                    
                    
                    
                    
                canvas.create_text(200, 60, text="press s to start another simulation", font="Arial 16 italic", fill="black")
        canvas.focus_set()
        canvas.bind("<Key>", clavier)
        window2.mainloop()

window = Tk()
Frame_1 = Frame(window, borderwidth=2, relief=GROOVE)
Frame_1.pack(side = LEFT,padx=30,pady=30)
Frame_2 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_2.pack(side=LEFT,padx=30,pady=30)
Frame_3 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_3.pack(side=LEFT,padx=30,pady=30)
Frame_4 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_4.pack(side=LEFT,padx=30,pady=30)
Frame_V = Frame(window, borderwidth=2, relief = GROOVE)
Frame_V.pack(side = BOTTOM)
label_1 = Label(Frame_1, text="largeur", bg="white", width = 12 ,height = 2)
label_1.pack()
value_1 = StringVar()
value_1.set(20)
enter_1 = Entry(Frame_1, textvariable=value_1, width=15)
enter_1.pack()
label_2 = Label(Frame_1, text="hauteur", bg="white",width = 12 ,height = 2)
label_2.pack()
value_2 = StringVar() 
value_2.set(20)
enter_2 = Entry(Frame_1, textvariable=value_2, width=15)
enter_2.pack()
label_3 = Label(Frame_2, text="nombre de créatures", bg="white",width = 22 ,height = 2)
label_3.pack()
value_3 = StringVar() 
value_3.set(10)
enter_3 = Entry(Frame_2, textvariable=value_3, width=15)
enter_3.pack()
label_4 = Label(Frame_2, text="échelle", bg="white",width = 12 ,height = 2)
label_4.pack()
value_4 = StringVar() 
value_4.set(0.5)
enter_4 = Entry(Frame_2, textvariable=value_4, width=15)
enter_4.pack()
label_5 = Label(Frame_3, text="nombres de jours à simuler", bg="white",width = 22 ,height = 2)
label_5.pack()
value_5 = StringVar()
value_5.set(50)
enter_5 = Entry(Frame_3, textvariable=value_5, width=15)
enter_5.pack()
label_6 = Label(Frame_3, text="durée d'une heure", bg="white",width = 22 ,height = 2)
label_6.pack()
value_6 = StringVar()
value_6.set(0.1)
enter_6 = Entry(Frame_3, textvariable=value_6, width=15)
enter_6.pack()
label_7 = Label(Frame_4, text="affichage graphique", bg="white",width = 22 ,height = 2)
label_7.pack()
value_7 = StringVar()
value_7.set(1)
but_0 = Radiobutton(Frame_4, text="jamais", variable = value_7, value=0)
but_1 = Radiobutton(Frame_4, text="tous les jours", variable = value_7, value=1)
but_2 = Radiobutton(Frame_4, text="tous les 5 jours", variable = value_7, value=5)
but_3 = Radiobutton(Frame_4, text="tous les 10 jours", variable = value_7, value=10)

but_0.pack()
but_1.pack()
but_2.pack()
but_3.pack()

but_1 = Button(Frame_V, text="Valider", command=recup)
but_1.pack()
window.mainloop()