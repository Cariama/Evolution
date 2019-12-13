from tkinter import *
import time
from Evol_J import Evol
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
    echelle = float(enter_4.get())
    nsimulation = int(enter_5.get())
    A = Evol(nombre_de_creature,largeur,hauteur)
    B = display(A,echelle,nsimulation)
    B.launch()
    
class display :
    def __init__(self,class_in,scale,number_of_day) :
        self.scale = scale
        self.class_in = class_in
        self.Nod = number_of_day
    def launch(self) :
        window2 = Tk()
        canvas = Canvas(window2, width=(self.class_in.x-1)*100*self.scale,height = (self.class_in.y-1)*100*self.scale, background = "white")
        for i in self.class_in.entities :
            canvas.create_oval((i[0][0]-0.5)*100*self.scale,(i[0][1]-0.5)*100*self.scale,(i[0][0]+0.5)*100*self.scale,(i[0][1]+0.5)*100*self.scale,fill = "#555555")
        canvas.create_text(200, 60, text="press s to start the simulation", font="Arial 16 italic", fill="black")
        canvas.pack()
        def clavier(event):
            touche = event.keysym
            if touche == "s":
                for i in range(self.Nod) :
                    self.class_in.move()
                    while self.class_in.t < self.class_in.t_day :
                        canvas.delete(ALL)
                        self.class_in.move()
                        for index,i in enumerate(self.class_in.entities) :
                            canvas.create_oval( (i[0][0]-0.5)*100*self.scale, (i[0][1]-0.5)*100*self.scale, (i[0][0]+0.5)*100*self.scale, (i[0][1]+0.5)*100*self.scale,fill = my_random_colours[index])
                        for j in self.class_in.food :
                            canvas.create_oval( (j[0]-0.125)*100*self.scale, (j[1]-0.125)*100*self.scale, (j[0]+0.125)*100*self.scale, (j[1]+0.125)*100*self.scale,fill = "#005500")
                        time.sleep(0.1)
                        canvas.create_text(50, 20, text="hour : {}".format(self.class_in.t), font="Arial 16 italic", fill="black")
                        canvas.update()
        canvas.focus_set()
        canvas.bind("<Key>", clavier)
        window2.mainloop()

window = Tk()
label_1 = Label(window, text="largeur", bg="white", width = 12 ,height = 2)
label_1.pack()
value_1 = StringVar()
enter_1 = Entry(window, textvariable=value_1, width=25)
enter_1.pack()
label_2 = Label(window, text="hauteur", bg="white",width = 12 ,height = 2)
label_2.pack()
value_2 = StringVar() 
enter_2 = Entry(window, textvariable=value_2, width=25)
enter_2.pack()
label_3 = Label(window, text="nombre de créatures", bg="white",width = 22 ,height = 2)
label_3.pack()
value_3 = StringVar() 
enter_3 = Entry(window, textvariable=value_3, width=25)
enter_3.pack()
label_4 = Label(window, text="échelle", bg="white",width = 12 ,height = 2)
label_4.pack()
value_4 = StringVar() 
enter_4 = Entry(window, textvariable=value_4, width=25)
enter_4.pack()
label_5 = Label(window, text="nombres de jours à simuler", bg="white",width = 22 ,height = 2)
label_5.pack()
value_5 = StringVar() 
enter_5 = Entry(window, textvariable=value_5, width=25)
enter_5.pack()

but_1 = Button(window, text="Valider", command=recup)
but_1.pack()
window.mainloop()
