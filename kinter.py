from tkinter import *
import time
from Evlove_q_1 import Evol
import random

def get_colour():
    nn = int(random.random()*0xFFFFFF)
    return "#"+(8-len(hex(nn)))*"0"+hex(nn)[2:]
    
my_random_colours =[get_colour() for i in range(1000)]
#print(random_colours)



class affichage :
    def __init__(self,class_in,scale) :
        self.scale = scale
        self.class_in = class_in

    def launch(self) :
        def clavier(event):
            touche = event.keysym
            if touche == "s":
                while self.class_in.t <= self.class_in.t_day :
                    canvas.delete(ALL)
                    A.move()
                    for index,i in enumerate(self.class_in.entities) :
                        canvas.create_oval( (i[0][0]-0.5)*100*self.scale, (i[0][1]-0.5)*100*self.scale, (i[0][0]+0.5)*100*self.scale, (i[0][1]+0.5)*100*self.scale,fill = my_random_colours[index])
                    for j in A.food :
                        canvas.create_oval( (j[0]-0.125)*100*self.scale, (j[1]-0.125)*100*self.scale, (j[0]+0.125)*100*self.scale, (j[1]+0.125)*100*self.scale,fill = "#005500")
                    time.sleep(0.3)
                    canvas.create_text(50, 20, text="hour : {}".format(A.t), font="Arial 16 italic", fill="black")
                    canvas.update()
        window = Tk()
        canvas = Canvas(window, width=(A.x-1)*100*self.scale,height = (A.y-1)*100*self.scale, background = "white")
        
        for i in self.class_in.entities :
            canvas.create_oval((i[0][0]-0.5)*100*self.scale,(i[0][1]-0.5)*100*self.scale,(i[0][0]+0.5)*100*self.scale,(i[0][1]+0.5)*100*self.scale,fill = "#555555")
        canvas.focus_set()
        canvas.create_text(200, 60, text="press s to start the simulation", font="Arial 16 italic", fill="black")

        
        canvas.bind("<Key>", clavier)
        canvas.pack()
        window.mainloop()
if __name__ == "__main__":
    A = Evol(20,20,11)
    param = affichage(A,0.5)
    param.launch()
