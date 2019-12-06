from tkinter import *
import time
from Evlove import Evol

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
                    for i in self.class_in.entities :
                        canvas.create_oval( (i[0][0]-0.5)*100*self.scale, (i[0][1]-0.5)*100*self.scale, (i[0][0]+0.5)*100*self.scale, (i[0][1]+0.5)*100*self.scale,fill = "#555555")
                    for j in A.food :
                        canvas.create_oval( (j[0]-0.125)*100*self.scale, (j[1]-0.125)*100*self.scale, (j[0]+0.125)*100*self.scale, (j[1]+0.125)*100*self.scale,fill = "#005500")
                    time.sleep(0.1)
                    canvas.update()
                    self.class_in. t+= 1
            if touche == "p" :
                pass
        window = Tk()
        canvas = Canvas(window, width=(A.x-1)*100*self.scale,height = (A.y-1)*100*self.scale, background = "white")
        
        for i in self.class_in.entities :
            ball = canvas.create_oval((i[0][0]-0.5)*100*self.scale,(i[0][1]-0.5)*100*self.scale,(i[0][0]+0.5)*100*self.scale,(i[0][1]+0.5)*100*self.scale,fill = "#555555")
        canvas.focus_set()
        txt = canvas.create_text(200, 60, text="press s to start the simulation, p for pause", font="Arial 16 italic", fill="black")
        
        canvas.bind("<Key>", clavier)
        canvas.pack()
        window.mainloop()
if __name__ == "__main__":
    A = Evol(8,20,11)
    param = affichage(A,0.5)
    param.launch()