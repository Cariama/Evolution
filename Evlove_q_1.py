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
        sence=2.58
        r_hitbox=0.5
        self.t_day=24 #temps d'une journée
        self.t=0 #temps actuel
        self.food_hitbox=0.125
        self.entities=[[start_loc[i],Evol.base_direction(self,start_loc[i])+Evol.move_direction(), Evol.rand_speed(1),r_hitbox,rd.randint(1,10),0,sence,str(i)]for i in range(n_entities)] 
#        (0(position),1(angle de la direction),(2)speed,(3)rayon hitbox,(4)énergie de base,(5)comportement,(6)sense,(-1)repr)
#        print(self.entities)
        
    def speedDirection(teta):
        return np.array([np.cos(teta),np.sin(teta)])
    
    def dup(self,entity):
#        (0(position),1(angle de la direction),(2)speed,(3)rayon hitbox,(4)énergie de base,(5)comportement, sense (-1)repr)
        new_entity=(entity[0],Evol.base_direction(self,entity[0])+Evol.move_direction(),Evol.rand_speed(entity[2]),entity[4]/2,0,entity[6],'@')
        self.entities.append(new_entity)
        entity[4]=entity[4]/2
        #!!!penser à rajouter les trucs
        
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
        free_oy=[np.array([float(xi),0]) for xi in range(0,self.x-1)]
        free_ox=[np.array([0,float(yi)]) for yi in range(1,self.y-1)]
        free_my=[np.array([float(xi),float(self.y-1)]) for xi in range(1,self.x-1)]
        free_mx=[np.array([float(self.x-1),float(yi)]) for yi in range(1,self.y-2)]
        return rd.sample(free_oy,oy)+rd.sample(free_ox,ox)+rd.sample(free_mx,mx)+rd.sample(free_my,my)
    
    def food_init(self):#définit les emplacements de la nourritures
        l=[]
        for xi in range(1,self.x-1):
            for yi in range(1,self.y-1):
                l.append(np.array([xi,yi]))
        n_food=int(((self.x-2)*(self.y-2)/4)+0.5)
        return rd.sample(l,n_food)
    
    def isin(elem, liste):
        return np.array([(item == elem).all() for item in liste]).any()

    def food_pop(self):
        n_food2pop=int((len(self.food)/3)+0.5)
        if n_food2pop==0 and self.food!=[]: n_food2pop=1
#        print(n_food2pop)
        l=[]
        for xi in range(1,self.x-1):
            for yi in range(1,self.y-1):
                if Evol.isin(np.array([xi,yi]),self.food)==False:
                    for entity in self.entities:
                        if Evol.dist(entity[0],[xi,yi])> entity[3]+self.food_hitbox:
                            l.append(np.array([xi,yi]))
        self.food=self.food+rd.sample(l,min(len(l),n_food2pop))
    
    def moveToward(self,entity,coo):
        direction= coo-entity[0]/Evol.dist(entity[0],coo)
        vitesse=min(Evol.dist(entity[0],coo)-entity[3]-self.food_hitbox,entity[2])
        entity[0]=entity[0]+direction*vitesse
        entity[4]=entity[4]-0.25*vitesse
    
    def scanForFood(self,entity):
        vision=entity[6]
        the_miam=False
        for miam in self.food:
            d=self.x**2+self.y**2
            di=Evol.dist(miam,entity[0])+self.food_hitbox
            if d<=vision and di<d:
                d=di
                the_miam=miam
        return the_miam
    
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
        return np.sqrt(np.sum((coo_2-coo_1)**2))
    
    def anti_exit(self,entity):#empêche les créatures de sortir du cadre
        if entity[0][0]<0:
            entity[0][0]=0
            entity[1]=0
        elif entity[0][0]>self.x-1:
            entity[0][0]=self.x-1
            entity[1]=np.pi
        if entity[0][1]<0:
            entity[0][1]=0
            entity[1]=np.pi/2
        elif entity[0][1]>self.y-1:
            entity[0][1]=self.y-1
            entity[1]=-np.pi/2

    def go_home(self,entity) :
        dist_up = entity[0][1]
        dist_down = self.y - entity[0][1]
        dist_right = self.x - entity[0][0]
        dist_left = entity[0][0]
        if (dist_up - dist_down)**2 >= (dist_right - dist_left)**2 :
            entity[1] = (-1)**((dist_up - dist_down)<0)*np.pi/2
        else :
            entity[1] = ((dist_right - dist_left)>0)*np.pi

    def kill(self) :
        lenght = len(self.entities)
        for i, entity in enumerate(reversed(self.entities)) :
            if entity[0][0] < self.x-1.1 and entity[0][0] > 0.1 and entity[0][1] < self.y - 1.1 and entity[0][1] > 0 :
                del(self.entities[lenght - i - 1])    def move(self):
    def move(self):
        #Déplacement de base
        for entity in self.entities:
            if entity[5] != 3 or entity[5] != 4 :
                entity[0]=entity[0]+entity[2]*Evol.speedDirection(entity[1])
                Evol.anti_exit(self,entity)
                entity[4]-=0.25*entity[2]
#        #Si ils se touchent
#        for i1 in range(len(self.entities)):
#            for i2 in range(i1+1,len(self.entities)):
#                if Evol.dist(self.entities[i1][0],self.entities[i2][0])<self.entities[i1][3]+self.entities[i2][3]:
#                    print("boom")
#                    self.entities[i2][1],self.entities[i1][1]=self.entities[i1][1],self.entities[i2][1]
#                    self.entities[i1][0]=self.entities[i1][0]+self.entities[i1][2]*Evol.speedDirection(self.entities[i1][1])
#                    self.entities[i2][0]=self.entities[i2][0]+self.entities[i2][2]*Evol.speedDirection(self.entities[i2][1])
#                    Evol.anti_exit(self,self.entities[i1])
#                    Evol.anti_exit(self,self.entities[i2])
        #modifier les direction
        for entity in self.entities:
            if entity[5] == 0 :
                if entity[4] >= 15*0.25*entity[2] or self.t >= self.t_day*0.75 :
                    self.go_home(entity)
                entity[1]=entity[1]+Evol.move_direction()
        #se nourrire
        l=[]    
        for y in reversed(range(len(self.food))):
            d=self.x**2+self.y**2
            for i in range(len(self.entities)):
                di=Evol.dist(self.food[y],self.entities[i][0])
                if di<=self.food_hitbox+self.entities[i][3] and di<d:
                    d=di
                    ent=i
            if d<self.x**2+self.y**2:
#                print(self.entities[ent][-1],":miam")
                self.entities[ent][4]+=1
                del self.food[y]
        #temps
        self.t=self.t+1
        print(self.t)
        #mort
        i=0
        l=[]
        for entity in self.entities:
            if entity[4]<=0:
                l.append(i)
                print(entity[-1],":meurt")
            i+=1
        for ii in reversed(l):
            del self.entities[ii]    
        #repop des pommes
        if self.t >= self.t_day:
            print("day")
            self.kill()
            self.t=0
            Evol.food_pop(self)
            for entity in self.entities :
                entity[5] = 0
            
        #changement de comportement
        for entity in self.entities :
            if entity[4] >= max([self.x,self.y])*0.25*entity[2] + 5 or self.t >= self.t_day*0.75 :
                self.go_home(entity)
                entity[5] = 1
            elif self.t >= self.t_day*0.75 :
                self.go_home(entity)
                entity[5] = 2

    
    def __repr__(self):
        done=False
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
    
    def test(self):
        print(self.entities)
    

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
