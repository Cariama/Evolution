from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import time
from statistics import mean
from statistics import variance
from Simulation import Evol
import random


def recup() :
    """fonction qui récupère les données de l'interface et les réinjecte dans le lancement de l'affichage"""
    largeur = int(enter_1.get())
    hauteur = int(enter_2.get())
    nombre_de_creature = int(enter_3.get())
    rapport_bouffe = float(enter_8.get())
    day = int(value_9.get())
    rp = 1-float(value_11.get()) #ce 1 - n'est là qu'à cause de la construction de la fonction feed et nearest_food
    if value_12.get() == 1 :
        def conso(speed, hitbox, sence) :
            value = 0.25*speed*np.pi*hitbox**2*np.sqrt(sence)
            return value
    if value_12.get() == 2 :
        def conso(speed, hitbox, sence) :
            value = 0.2*speed**2*np.pi*hitbox**2 + 0.15*np.sqrt(sence)
            return value
    if value_12.get() == 3 :
        def conso(speed, hitbox, sence) :
            value = 0.15*speed**2 + 0.15*np.pi*hitbox**2 + 0.15*np.sqrt(sence)
            return value
    #création de la classe evol avec les coordonnées récupérées par l'interface et lancement de l'affichage
    A = Evol(nombre_de_creature,largeur,hauteur,rapport_nourriture=rapport_bouffe,t_day=day,rapport_predation= rp, V1 = variable_1.get(), V2=variable_2.get(), V3 = variable_3.get(), func = conso)
    B = display(A)
    B.launch()
    
class display :
    def __init__(self,class_in) : 
        """dans cette fonction init, d'autres valeurs sont récupérés de l'interface"""
        self.scale = float(enter_4.get())
        self.class_in = class_in
        self.Nod = int(enter_5.get()) #number of day
        self.frame = float(enter_6.get())
        self.x = 1 #cette variable est exactement le numéro du jour en cour (self.class_in.day), nous avons juste 2 variables différentes car c'est plus pratique pour la création des graphiques
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(221)
        plt.title("nombre de créatures")
        self.ax2 = self.fig.add_subplot(222)
        plt.title("vitesse moyenne")
        self.ax3 = self.fig.add_subplot(223)
        plt.title("taille moyenne")
        self.ax4 = self.fig.add_subplot(224)
        plt.title("portée moyenne")
        self.ax2.set_ylim(0,4)
        self.ax3.set_ylim(0,2)
        self.ax4.set_ylim(0,3)
        self.factor = int(value_7.get()) #facteur qui active ou non l'affichage dynamique
    
    def launch(self) :
        """fonction qui lance l'affichage"""
        if self.factor==0 :
            for i in range(self.Nod) :
                self.class_in.move() #cette fonction move fait avancer l'heure à la fin de la journée (sauf lors du premier jour) ce qui active le changement de jour et la reproduction. Sans elle, la simulation reste bloquée à la première journée.
                while self.class_in.t < self.class_in.t_day-1 : #comme notre code remet l'heure à 0 à la fin de la journée, il faut rajouter un -1 afin que le code ne rentre pas dans une boucle infinie
                    self.class_in.move()
                y1 = len(self.class_in.creatures)
                self.ax1.plot(self.x,y1,"g^")
                speed_list = []
                size_list = []
                sence_list = []
                for crea in self.class_in.creatures :
                    speed_list += [crea.speed]
                    size_list += [crea.hitbox]
                    sence_list += [crea.sence]
                y2 = mean(speed_list)
                y2_ = variance(speed_list)
                self.ax2.plot(self.x,y2,"r^")
                self.ax2.errorbar(self.x,y2,y2_,color="black")
                y3 = mean(size_list)
                y3_ = variance(size_list)
                self.ax3.plot(self.x,y3,"go")
                self.ax3.errorbar(self.x,y3,y3_,color="black")
                y4 = mean(sence_list)
                y4_ = variance(sence_list)
                self.ax4.plot(self.x,y4,"bo")
                self.ax4.errorbar(self.x,y4,y4_,color="black")
                plt.pause(0.000005)
                self.x += 1
        else :
            window2 = Tk()
            canvas = Canvas(window2, width=(self.class_in.x)*100*self.scale,height = (self.class_in.y)*100*self.scale, background = "white") #création de la fenêtre d'affichage graphique
            for crea in self.class_in.creatures :
                canvas.create_oval((crea.position[0]-0.5)*100*self.scale,(crea.position[1]-0.5)*100*self.scale,(crea.position[0]+0.5)*100*self.scale,(crea.position[1]+0.5)*100*self.scale,fill = "#555555")
            canvas.create_text(200, 60, text="press s to start the simulation", font="Arial 16 italic", fill="black")
            canvas.pack()
            def clavier(event):
                touche = event.keysym
                if touche == "s":
                    for i in range(self.Nod) :
                        self.class_in.move()
                        list_of_gen = [] #cette liste nous sera utile pour trouver la génération la plus jeune (plus de détails dans le fichier READ_ME)
                        for crea in self.class_in.creatures :
                            list_of_gen += [crea.gen]
                        while self.class_in.t < self.class_in.t_day-1 :
                            self.class_in.move()
                            if (self.class_in.day%self.factor) == 0 :
                                canvas.delete(ALL)
                                for index,crea in enumerate(self.class_in.creatures) :
                                    canvas.create_oval( (crea.position[0]-crea.hitbox)*100*self.scale, (crea.position[1]-crea.hitbox)*100*self.scale, (crea.position[0]+crea.hitbox)*100*self.scale, (crea.position[1]+crea.hitbox)*100*self.scale,fill = crea.colour)
                                for apple in self.class_in.foods :
                                    canvas.create_oval( (apple[0]-0.125)*100*self.scale, (apple[1]-0.125)*100*self.scale, (apple[0]+0.125)*100*self.scale, (apple[1]+0.125)*100*self.scale,fill = "#005500")
                                time.sleep(self.frame)
                                canvas.create_text(130, 50, text="hour : {}\nday : {}\npopulation : {}\ndernière génération : {}".format(self.class_in.t,self.class_in.day,len(self.class_in.creatures), max(list_of_gen)), font="Arial 16 italic", fill="black")
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
                        y2_ = variance(speed_list)
                        self.ax2.plot(self.x,y2,"r^")
                        self.ax2.errorbar(self.x,y2,y2_,color="black")
                        y3 = mean(size_list)
                        y3_ = variance(size_list)
                        self.ax3.plot(self.x,y3,"go")
                        self.ax3.errorbar(self.x,y3,y3_,color="black")
                        y4 = mean(sence_list)
                        y4_ = variance(sence_list)
                        self.ax4.plot(self.x,y4,"bo")
                        self.ax4.errorbar(self.x,y4,y4_,color="black")
                        plt.pause(0.000005)
                        self.x += 1
                    
                canvas.create_text(200, 60, text="press s to start another simulation", font="Arial 16 italic", fill="black")
        canvas.focus_set()
        canvas.bind("<Key>", clavier)
        window2.mainloop()

#La suite du code est très lourde. Elle sert à créer l'interface pour définir les conditions initiales.
#Il ne faut pas se fier aux numéros, nous avons intégré chaque windget au fur et à mesure et les numéros ne sont que des indexes

window = Tk()

Frame_1 = Frame(window, borderwidth=2, relief=GROOVE)
Frame_1.pack(side = LEFT,padx=30,pady=30)

Frame_2 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_2.pack(side=LEFT,padx=30,pady=30)

Frame_3 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_3.pack(side=LEFT,padx=30,pady=30)

Frame_4 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_4.pack(side=LEFT,padx=30,pady=30)

Frame_5 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_5.pack(side=LEFT,padx=30,pady=30)

Frame_6 = Frame(window, borderwidth=2, relief = GROOVE)
Frame_6.pack(side=LEFT,padx=30,pady=30)


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
value_3.set(50)
enter_3 = Entry(Frame_2, textvariable=value_3, width=15)
enter_3.pack()

label_4 = Label(Frame_1, text="échelle", bg="white",width = 12 ,height = 2)
label_4.pack()
value_4 = StringVar() 
value_4.set(0.3)
enter_4 = Entry(Frame_1, textvariable=value_4, width=15)
enter_4.pack()

label_5 = Label(Frame_2, text="nombres de jours à simuler", bg="white",width = 22 ,height = 2)
label_5.pack()
value_5 = StringVar()
value_5.set(100)
enter_5 = Entry(Frame_2, textvariable=value_5, width=15)
enter_5.pack()

label_6 = Label(Frame_2, text="durée d'une heure", bg="white",width = 22 ,height = 2)
label_6.pack()
value_6 = StringVar()
value_6.set(0.1)
enter_6 = Entry(Frame_2, textvariable=value_6, width=15)
enter_6.pack()

label_7 = Label(Frame_3, text="affichage dynamique", bg="white",width = 22 ,height = 2)
label_7.pack()
value_7 = StringVar()
value_7.set(1)

but_0 = Radiobutton(Frame_3, text="jamais", variable = value_7, value=0)
but_1 = Radiobutton(Frame_3, text="tous les jours", variable = value_7, value=1)
but_2 = Radiobutton(Frame_3, text="tous les 5 jours", variable = value_7, value=5)
but_3 = Radiobutton(Frame_3, text="tous les 10 jours", variable = value_7, value=10)

but_0.pack()
but_1.pack()
but_2.pack()
but_3.pack()

label_8 = Label(Frame_4, text="rapport de nourriture", bg="white",width = 22 ,height = 2)
label_8.pack()
value_8 = StringVar()
value_8.set(0.2)
enter_8 = Entry(Frame_4, textvariable=value_8, width=15)
enter_8.pack()

label_9 = Label(Frame_2, text="durée d'une journée", bg="white",width = 22 ,height = 2)
label_9.pack()
value_9 = StringVar()
value_9.set(24)
enter_9 = Entry(Frame_2, textvariable=value_9, width=15)
enter_9.pack()

label_10 = Label(Frame_6, text="mutations autorisées", bg="white",width = 22 ,height = 2)
label_10.pack()

variable_1 = IntVar()
variable_2 = IntVar()
variable_3 = IntVar()
variable_1.set(1)
variable_2.set(1)
variable_3.set(1)

but_4 = Checkbutton(Frame_6,text="vitesse",variable=variable_1)
but_5 = Checkbutton(Frame_6,text="taille",variable=variable_2)
but_6 = Checkbutton(Frame_6,text="détection",variable=variable_3)

but_4.pack()
but_5.pack()
but_6.pack()

label_11 = Label(Frame_4, text="rapport de prédation", bg="white",width = 22 ,height = 2)
label_11.pack()
value_11 = StringVar()
value_11.set(0.58)
enter_11 = Entry(Frame_4, textvariable=value_11, width=15)
enter_11.pack()

label_12 = Label(Frame_5, text="formule de consomation", bg="white",width = 22 ,height = 2)
label_12.pack()
value_12 = IntVar()
value_12.set(1)

but_7 = Radiobutton(Frame_5, text="0,25.vitesse.pi.taille².détection", variable = value_12, value=1)
but_8 = Radiobutton(Frame_5, text="0,2.vitesse².pi.taille² + 0,2.(racine de vue)", variable = value_12, value=2)
but_9 = Radiobutton(Frame_5, text="0,15.vitesse² + 0,15.pi.taille² + 0,2.(racine de vue)", variable = value_12, value=3)

but_7.pack()
but_8.pack()
but_9.pack()



but_V = Button(window,text="Valider", command=recup,width=30,height=3)
but_V.pack()
but_V.place(x=1200,y=200)



window.mainloop()
