import numpy as np
import random as rd
#0------>
#|       y
#|
#|
#v x
class Evol:
    def __init__(self,n_entities,x,y):
        self.x,self.y=x,y #plateau
        self.n_entities=n_entities
        self.food=Evol.food_init(self)#liste des coo des pommes
        start_loc=Evol.init_location(self)
        r_hitbox=0.5
        self.t_day=24 #temps d'une journée
        self.t=0 #temps actuel
        self.food_hitbox=0.125
        stock_miam=0
        self.entities=[[start_loc[i],Evol.base_direction(self,start_loc[i])+Evol.move_direction(), Evol.rand_speed(1),r_hitbox,stock_miam,str(i)]for i in range(n_entities)] 
#        ((position),(angle de la direction),speed,rayon hitbox,stock de nourriture, repr)
#        print(self.entities)
    def test(self):
        print(self.entities)
        
    def rand_speed(base):#défini les vitesse de base des créatures
        return abs(base+rd.gauss(0,0.7))
    
    def init_location(self):
        oy,ox,my,mx=0,0,0,0 #oy:y=0, ox:x=0, my:y=max, mx:x=max
        for i in range(self.n_entities):#distribue les creatures par coté
            if i%4==0:
                oy+=1
            elif (i-1)%4==0:
                ox+=1
            elif i%2==0:
                my+=1
            elif (i-1)%2==0:
                mx+=1
        free_oy=[[float(xi),0] for xi in range(0,self.x-1)]
        free_ox=[[0,float(yi)] for yi in range(1,self.y-1)]
        free_my=[[float(xi),float(self.y-1)] for xi in range(1,self.x-1)]
        free_mx=[[float(self.x-1),float(yi)] for yi in range(1,self.y-2)]
        return rd.sample(free_oy,oy)+rd.sample(free_ox,ox)+rd.sample(free_mx,mx)+rd.sample(free_my,my)
    
    def food_init(self):#définit les emplacements de la nourritures
        l=[]
        for xi in range(1,self.x-1):
            for yi in range(1,self.y-1):
                l.append([xi,yi])
        n_food=int(((self.x-2)*(self.y-2)/4)+0.5)
        return rd.sample(l,n_food)
    
    def food_pop(self):
        n_food2pop=int((len(self.food)/3)+0.5)
        if n_food2pop==0 and self.food!=[]: n_food2pop=1
        print(n_food2pop)
        l=[]
        for xi in range(1,self.x-1):
            for yi in range(1,self.y-1):
                if [xi,yi] not in self.food:
                    l.append([xi,yi])
#        print(l)
        for entity in self.entities:
            if Evol.dist(entity[0],[xi,yi])<= entity[3]+self.food_hitbox:
                l.remove([xi,yi])
#        print(l)
#        print("food before:",self.food)
        self.food=self.food+rd.sample(l,min(len(l),n_food2pop))
#        print("food after:",self.food)
        
    def move_direction():#modifie potentiellement l'angle de la direction
        if rd.random()<0.8:
            return rd.gauss(0,1)
        else:
            return(0)
    
    def base_direction(self,location):#défini la direction de base
        if location[0]==0:
            return 0
        if location [0]==self.x-1:
            return np.pi
        if location[1]==0:
            return np.pi/2
        if location [1]==self.y-1:
            return -(np.pi/2)
        
    def dist(coo_1,coo_2):#calcule les distance
        x1=coo_1[0]
        x2=coo_2[0]
        y1=coo_1[1]
        y2=coo_2[1]
#        print("dist",coo_1,coo_2,np.sqrt((x2-x1)**2+(y2-y1)**2))
        return np.sqrt((x2-x1)**2+(y2-y1)**2)
    def anti_exit(self,entity):#empêche les créatures de sortir du cadre
        if entity[0][0]<0:
            entity[0][0]=0
        elif entity[0][0]>self.x-1:
            entity[0][0]=self.x-1
        if entity[0][1]<0:
            entity[0][1]=0
        elif entity[0][1]>self.y-1:
            entity[0][1]=self.y-1
            
    def move(self):
        #Déplacement de base
        for entity in self.entities:
            entity[0][0]=entity[0][0]+entity[2]*np.cos(entity[1])
            entity[0][1]=entity[0][1]+entity[2]*np.sin(entity[1])
            Evol.anti_exit(self,entity)
        #Si ils se touchent
        for i1 in range(len(self.entities)):
            for i2 in range(i1+1,len(self.entities)):
                if Evol.dist(self.entities[i1][0],self.entities[i2][0])<self.entities[i1][3]+self.entities[i2][3]:
#                    print("niah")
                    self.entities[i1][0][0]=self.entities[i1][0][0]+self.entities[i1][2]*np.cos(self.entities[i2][1])
                    self.entities[i1][0][1]=self.entities[i1][0][1]+self.entities[i1][2]*np.sin(self.entities[i2][1])
                    self.entities[i2][0][0]=self.entities[i2][0][0]+self.entities[i2][2]*np.cos(self.entities[i1][1])
                    self.entities[i2][0][1]=self.entities[i2][0][1]+self.entities[i2][2]*np.sin(self.entities[i1][1])
                    Evol.anti_exit(self,self.entities[i1])
                    Evol.anti_exit(self,self.entities[i2])
        #modifier les direction
        for entity in self.entities:
            entity[1]=entity[1]+Evol.move_direction()
        #se nourrire
        l=[]    
        for miam in self.food:
            d=self.x**2+self.y**2
            for i in range(len(self.entities)):
                di=Evol.dist(miam,self.entities[i][0])
                if di<=self.food_hitbox+self.entities[i][3] and di<d:
                    d=di
                    ent=i
            if d<self.x**2+self.y**2:
#                print(self.entities[ent][-1],":miam")
                self.entities[ent][4]+=1
                l.append(miam)
        for i in l:
            self.food.remove(i)
        self.t=self.t+1
        #repop des pommes
        if self.t >= self.t_day:
            print("day")
            self.t=0
            Evol.food_pop(self)
                    
    
    def __repr__(self):
        txt="+"+self.y*"–"+"+"
        for xi in range(self.x):
            txt+="\n|"
            for yi in range(self.y):
                for entity in self.entities:
                    done=False
                    if xi==int(entity[0][0]+0.5) and yi==int(entity[0][1]+0.5):
                        txt+=entity[-1]
                        done=True
                        break
                for miam in self.food:
                    if xi==miam[0] and yi == miam[1]:
                        txt+=""
                        done=True
                        break
                if done==False:
                    txt+=" "
            txt+="|"
        txt+="\n+"+self.y*"–"+"+"
        return txt
    

if __name__=="__main__":
    c=0
    print("-------")
    t=Evol(9,8,16)
    print(t)
    while True:
        a=input("q to quit: ")
        if a=="q":
            break
        elif a=="p":
            t.test()
        print("-------")
        t.move()
        c+=1
        print(t)
        if t.food==[]:
            for entity in t.entities:
                print(entity[-1],":",entity[4])
            print("turn:",c)
#note: food en continu? comment? Voir plus tard
#remplacer les assignation de coodonée avec random sample
#question: Entity devrait-elle avoir une donnée sigma pour move_direction()?
#bouffe->manger->energie->mort