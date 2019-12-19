import numpy as np
import random as rd

class Creature:
    def __init__(self, position, angle, base_speed,base_energie, hitbox, sence,  generation=0, comportement=0,var1=1, var2=1, var3=1):
        self.position = position
        self.angle = angle + Creature.add_angle()
        if var1 :
            self.speed = Creature.abs_rd_gauss(base_speed, 0.3)
        else :
            self.speed = 1
        if var2 :
            self.hitbox = Creature.abs_rd_gauss(hitbox, 0.1)
            if self.hitbox < 0.05 :
                self.hitbox = 0.05
        else :
            self.hitbox=0.5
        self.energie = base_energie
        if var3 :
            self.sence = Creature.abs_rd_gauss(sence, 0.25)
        else :
            self.sence=1
        self.comp = comportement
        self.gen = generation
        ratio = 255/(self.speed + self.hitbox + self.sence)
        self.colour = Creature.rgb_to_hex((int(self.speed * ratio),int(self.hitbox * ratio), int(self.sence * ratio)))
        
    def rgb_to_hex(rgb):
        return "#"+str('%02x%02x%02x' % rgb)
        
    def direction(self):
        return np.array([np.cos(self.angle), np.sin(self.angle)])
    
    def add_angle():
        if rd.random() < 0.4:
            return rd.gauss(0, 0.3)
        
        else:
            return(0)
    
    def abs_rd_gauss(base_speed, sigma):
        return abs(base_speed + rd.gauss(0, sigma))
        
    def dist(self,coo):
        return np.sqrt(np.sum((self.position - coo) ** 2))
    
    def anti_exit(self, x_max, y_max):#! mettre les x/y max des coordonnées
        if self.position[0] < 0:
            self.position[0] = 0
            self.angle = 0 + Creature.add_angle()
            
        elif self.position[0] > x_max:
            self.position[0] = x_max
            self.angle = np.pi + Creature.add_angle()
            
        if self.position[1] < 0:
            self.position[1] = 0
            self.angle = np.pi * 0.5 + Creature.add_angle()
            
        elif self.position[1] > y_max:
            self.position[1] = y_max
            self.angle = -np.pi * 0.5 + Creature.add_angle()
            
    def nearest_food(self, foods, creatures, rp):
        d = 10**1000
        the_food=0
        for food in foods:
            di = Creature.dist(self,food)
            if di < d:
                d = di
                the_food = food
        for creature in creatures:
            if creature.hitbox ** 2< self.hitbox ** 2 * rp:
                di=Creature.dist(self, creature.position)
                if di < d:
                    d = di
                    the_food = creature.position
        return d, the_food
    
    def moveToward(self,coo):
        try:
            direction = (self.position-coo)/Creature.dist(self, coo)
            
        except ZeroDivisionError:
            direction = 0
        vitesse = min(self.speed, Creature.dist(self, coo))
        self.position += direction * vitesse
        self.energie -= 0.25 * vitesse * np.pi * self.hitbox ** 2
    
    def moving(self, foods, creatures, rp):
        d, the_food = Creature.nearest_food(self,foods, creatures, rp)
        if self.comp == 0 and d <= self.sence:
            Creature.moveToward(self, the_food)
            
        elif self.comp != 2:
            self.position += Creature.direction(self) * self.speed
            self.energie -= 0.25 * self.speed * np.pi * self.hitbox ** 2
            if self.comp == 0:
                self.angle += Creature.add_angle()
                
    def go_home(self, x, y) : #! mettre les x/y max des coordonnées
        dist_up = y  - self.position[1]
        dist_down = self.position[1]
        dist_right = x  - self.position[0]
        dist_left = self.position[0]
        list_ = [dist_right, dist_up, dist_left, dist_down]
        for i in range(4) :
            if list_[i] <= min(list_[:i]+list_[i+1:]) :
                self.angle = i*np.pi/2

#-------------------------

class Evol:
    def __init__(self, n_creatures, x, y, rapport_nourriture=0.2, rapport_predation=0.42, t_day=24):
        self.x, self.y = x, y
        self.rap_food = rapport_nourriture
        self.food_hitbox=0.125
        self.rp=rapport_predation
        self.foods = Evol.foods_init(self)
        start_loc, start_angle = Evol.init_states(self, n_creatures)
        self.creatures = [Creature(start_loc[i], start_angle[i], 1, rd.uniform(1,7), 0.5, rd.uniform(0.5, 2)) for i in range(n_creatures)]
        self.t = 0
        self.t_day = t_day
        self.day = 0
        
    def init_states(self, n_creatures):
        oy,ox,my,mx=0,0,0,0 #oy:y=0, ox:x=0, my:y=max, mx:x=max
        for i in range(n_creatures):#distribue les creatures sur les cotés
            if i % 4 == 0:
                oy += 1
                
            elif (i - 1) % 4 == 0:
                ox += 1
                
            elif i % 2 == 0:
                my += 1
                
            elif (i - 1) % 2 == 0:
                mx += 1

        oy_s = [np.array([rd.random() * self.x, 0]) for i in range(oy)]
        ox_s = [np.array([0, rd.random() * self.y]) for i in range(oy)]
        my_s = [np.array([rd.random() * self.x, float(self.y-1)]) for i in range(oy)]
        mx_s = [np.array([float(self.x-1), rd.random() * self.y]) for i in range(oy)]
        angles = [np.pi * 0.5 for i in range(oy)] + [0 for i in range(ox)] + [-np.pi * 0.5 for i in range(my)] + [np.pi for i in range(mx)]
        return oy_s + ox_s + my_s + mx_s, angles
    
    def foods_init(self):#définit les emplacements de la nourritures
        l=[]
        for xi in range(1, self.x-1):
            for yi in range(1, self.y-1):
                l.append(np.array([xi + rd.gauss(0, 0.35), yi + rd.gauss(0,0.35)]))
        n_food = int((self.x-2) * (self.y-2) * self.rap_food + 0.5)
        return rd.sample(l,n_food)
    
    def dup(self,crea):
        a = np.array([rd.uniform(-0.1, 0.1), rd.uniform(-0.1, 0.1)])
        new_crea = Creature(crea.position + a, crea.angle, crea.speed, crea.energie/2, crea.hitbox, crea.sence, generation = crea.gen + 1)
        new_crea.anti_exit(self.x-1, self.y-1)
        crea.energie /= 2
        return new_crea
    
    def feed(self):
        l=len(self.foods)
        for i, food in enumerate(reversed(self.foods)):
            d = (self.x * self.y) ** 2
            for ii, crea in enumerate(self.creatures):
                di = crea.dist(food)
                if di < d and di <= crea.hitbox + self.food_hitbox:
                    ent = ii
                    d = di
            if d < (self.x * self.y) ** 2:
                self.creatures[ent].energie += 5
                del self.foods[l - i - 1]    
        dead=[]        
        for i, crea1 in enumerate(self.creatures):
            l=[]
            for ii, crea2 in enumerate(self.creatures):
                if i != ii:
                    if crea1.dist(crea2.position) <= crea1.hitbox + crea2.hitbox:
                        if crea1.hitbox ** 2 < crea2.hitbox ** 2 * self.rp:
                            l.append(ii)
                            if i not in dead:
                                dead.append(i)
            for n in l:
                self.creatures[n].energie += crea1.hitbox * crea1.energie /(len(l) * 8)
        for i in reversed(dead):
            del self.creatures[i]
    
    def kill(self) :
        lenght = len(self.creatures)
        for i, crea in enumerate(reversed(self.creatures)) :
            if crea.position[0] < self.x-1.1 and crea.position[0] > 0.1 and crea.position[1] < self.y - 1.1 and crea.position[1] > 0 :
                del self.creatures[lenght - i - 1]
    
    def move(self):
        #Le temps défile
        self.t+=1
        #Deplcement
        for crea in self.creatures:
            crea.moving(self.foods, self.creatures, self.rp)
            crea.anti_exit(self.x-1, self.y-1)
        #Se nourrir
        Evol.feed(self) 
        #Mourir de faim
        l=len(self.creatures)
        for i, crea in enumerate(reversed(self.creatures)):
            if crea.energie<=0:
                del self.creatures[l-i-1]
        #Fin de journée
        if self.t>=self.t_day:
            self.t = 0
            self.day += 1
            Evol.kill(self)
            self.foods = Evol.foods_init(self)
            new_creatures=[]
            for crea in self.creatures:
                if crea.energie >= 25 * crea.hitbox ** 2:
                    new_creatures.append(Evol.dup(self, crea))
            self.creatures += new_creatures
            mini=self.creatures[0].gen
            maxi=0
            for crea in self.creatures:
                crea.comp = 0
#                crea.energie /= 2 #???
                if crea.gen<mini:
                    mini=crea.gen
                if crea.gen > maxi:
                    maxi=crea.gen
#            print(len(self.creatures))
#            print("min;",mini,"max:",maxi)
#            print("---------")
        #Changement de comportement
        for crea in self.creatures:
            if crea.comp == 0 and (crea.energie >= max([self.x, self.y]) * 0.25 * crea.speed + 25 * crea.hitbox ** 2 or self.t >= self.t_day*0.75):
                crea.go_home(self.x-1,self.x-2)
                crea.comp = 1
                
            if crea.comp == 1 and (crea.position[0] > self.x-1.1 or crea.position[0] < 0.1 or crea.position[1] > self.y - 1.1 or crea.position[1] < 0.1):
                crea.comp = 2
