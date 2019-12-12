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
        sence=[rd.uniform(0.5,2) for i in range(n_entities)]
        r_hitbox=0.5
        self.t_day=24 #temps d'une journée
        self.t=0 #temps actuel
        self.food_hitbox=0.125
        self.entities=[[start_loc[i],Evol.base_direction(self,start_loc[i])+Evol.move_direction(), Evol.rand_speed(1),r_hitbox,rd.randint(1,10),0,sence[i]]for i in range(n_entities)] 
#        (0(position),1(angle de la direction),(2)speed,(3)rayon hitbox,(4)énergie de base,(5)comportement,(6)sense)
#        print(self.entities[0])
     
    def dup(self,entity):
#        (0(position),1(angle de la direction),(2)speed,(3)rayon hitbox,(4)énergie de base,(5)comportement, sense (-1)repr)
        new_entity=[entity[0],Evol.base_direction(self,entity[0])+Evol.move_direction(),Evol.rand_speed(entity[2]),0.5,entity[4]/2,0,entity[6]]
        self.entities.append(new_entity)
#        print("new",new_entity)
#        print(self.entities[-1])
        entity[4]=entity[4]/2
        #!!!penser à rajouter les trucs
    
    def speedDirection(teta):
        return np.array([np.cos(teta),np.sin(teta)])
    
    def rand_speed(base):#défini les vitesse de base des créatures
        return abs(base+rd.gauss(0,0.3))
    
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
#
        oy_s=[np.array([rd.random()*self.x,0]) for i in range(oy)]
        ox_s=[np.array([0,rd.random()*self.y]) for i in range(oy)]
        my_s=[np.array([rd.random()*self.x,float(self.y-1)]) for i in range(oy)]
        mx_s=[np.array([float(self.x-1),rd.random()*self.y]) for i in range(oy)]
        return oy_s+ox_s+my_s+mx_s
    
    def food_init(self):#définit les emplacements de la nourritures
        l=[]
        for xi in range(1,self.x-1):
            for yi in range(1,self.y-1):
                l.append(np.array([xi+rd.gauss(0,0.35),yi+rd.gauss(0,0.35)]))
        n_food=int(((self.x-2)*(self.y-2)/4)+0.5)
        return rd.sample(l,n_food)
    
    def isin(elem, liste):
        return np.array([(item == elem).all() for item in liste]).any()

#    def food_pop(self):
#        n_food2pop=int((len(self.food)/3)+0.5)
#        if n_food2pop==0 and self.food!=[]: n_food2pop=1
##        print(n_food2pop)
#        l=[]
#        for xi in range(1,self.x-1):
#            for yi in range(1,self.y-1):
#                if Evol.isin(np.array([xi,yi]),self.food)==False:
#                    for entity in self.entities:
#                        if Evol.dist(entity[0],[xi,yi])> entity[3]+self.food_hitbox:
#                            l.append(np.array([xi,yi]))
#        self.food=self.food+rd.sample(l,min(len(l),n_food2pop))
    
    def moveToward(self,entity,coo):
        direction= (coo-entity[0])/Evol.dist(entity[0],coo)
        vitesse=min(Evol.dist(entity[0],coo),entity[2])
        entity[0]=entity[0]+direction*vitesse
        entity[4]=entity[4]-0.25*vitesse
    
    def move_direction():#modifie potentiellement l'angle de la direction
        if rd.random()<0.8:
            return rd.gauss(0,1)
        else:
            return(0)
    
    def base_direction(self,location):#défini la direction de base
        if location[0]<=1:
            return 0
        if location [0]>=self.x-2:
            return np.pi
        if location[1]<=1:
            return np.pi/2
        if location [1]>=self.y-2:
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
    
    def goForFood(self,entity):
        vision=entity[6]
        done=False
#        print("food?")
        for miam in self.food:
            d=self.x**2+self.y**2
            di=Evol.dist(miam,entity[0])+self.food_hitbox
            if di<=vision and di<d:
#                print("trouvé1")
                d=di
                the_miam=miam
                done=True
        if done==True:
            print(the_miam)
#            print("miam?")
            Evol.moveToward(self,entity,the_miam)
        return done
        
    def go_home(self,entity) :
        dist_up = self.y - 1 - entity[0][1]
        dist_down = entity[0][1]
        dist_right = self.x - 1 - entity[0][0]
        dist_left = entity[0][0]
        list_ = [dist_right,dist_up,dist_left,dist_down]
        for i in range(4) :
            if list_[i] <= min(list_[:i]+list_[i+1:]) :
                entity[1] = i*np.pi/2
            

    def kill(self) :
        lenght = len(self.entities)
        for i, entity in enumerate(reversed(self.entities)) :
            if entity[0][0] < self.x-1.1 and entity[0][0] > 0.1 and entity[0][1] < self.y - 1.1 and entity[0][1] > 0 :
                del(self.entities[lenght - i - 1])
                
    def move(self):
         #temps
        self.t=self.t+1
        
        #Déplacement de base
        for entity in self.entities:
            if entity[5]==2:
                if self.t>=self.t_day and entity[4]>=6:
#                    print("crac")
                    Evol.dup(self,entity)
            elif entity[5]==1:
                entity[0]=entity[0]+entity[2]*Evol.speedDirection(entity[1])
                entity[4]-=0.25*entity[2]
                Evol.anti_exit(self,entity)
            elif Evol.goForFood(self,entity):
#                print("bah",entity[-1])
                pass
            else:
#                print("else")
#                print(entity[-1])
                entity[0]=entity[0]+entity[2]*Evol.speedDirection(entity[1])
                Evol.anti_exit(self,entity)
                entity[4]-=0.25*entity[2]
                
        #Si ils se touchent
#        for i1 in range(len(self.entities)):
#            for i2 in range(i1+1,len(self.entities)):
#                if Evol.dist(self.entities[i1][0],self.entities[i2][0])<self.entities[i1][3]+self.entities[i2][3]:
##                    print("boom")
#                    self.entities[i2][1],self.entities[i1][1]=self.entities[i1][1],self.entities[i2][1]
#                    self.entities[i1][0]=self.entities[i1][0]+self.entities[i1][2]*Evol.speedDirection(self.entities[i1][1])
#                    self.entities[i2][0]=self.entities[i2][0]+self.entities[i2][2]*Evol.speedDirection(self.entities[i2][1])
#                    Evol.anti_exit(self,self.entities[i1])
#                    Evol.anti_exit(self,self.entities[i2])
        #modifier les direction
        for entity in self.entities:
            if entity[5] == 0 :
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
                self.entities[ent][4]+=5
                del self.food[y]
       
        #se reproduire
        for entity in self.entities:
            if entity[5]==2:
                if entity[4]>=17 and self.t>=self.t_day:
#                    print("crac")
                    Evol.dup(self,entity)
       
        #mort de faim
        i=0
        l=[]
        for entity in self.entities:
            if entity[4]<=0:
                l.append(i)
#                print(entity[-1],":meurt")
            i+=1
        for ii in reversed(l):
            del self.entities[ii]  
            
        #repop des pommes
        if self.t >= self.t_day:
#            print("day")
            self.kill()
            self.t=0
            self.food=Evol.food_init(self)
#            Evol.food_pop(self)
            for entity in self.entities :
                entity[5] = 0
                entity[4] -= entity[4]/2
#            
        #changement de comportement
        for entity in self.entities :
            if entity[5] == 0 :
                if entity[4] >= max([self.x,self.y])*0.25*entity[2] + 17 or self.t >= self.t_day*0.75 :
                    self.go_home(entity)
                    entity[5] = 1
            if entity[5] == 1 and (entity[0][0] > self.x-1.1 or entity[0][0] < 0.1 or entity[0][1] > self.y - 1.1 or entity[0][1] < 0.1) :
                entity[5] = 2
        
    def test(self):
        for entity in self.entities:
            print(entity[6])
            
if __name__ == "__main__":
    t=Evol(10,10,10)
    t.test()
