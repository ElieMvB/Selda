import pyxel
from random import randint
from bin.monster import*

class Waves:
    #the point is to make it really easy to spawn a wave from the Game class
    def __init__(self, w):
        self.wave = w
        self.monster_list = []
    
    def spawn(self):
        #spawns monsters
        #only 2 every second
        if pyxel.frame_count % 30 == 0 and len(self.monster_list) <= 0 + self.wave - 1:
            x = randint(0, 128)
            y = randint(0, 128)
            while not((y <= 25 or y >= 95) or (x <= 25 or x >= 95)):
                x = randint(0, 128)
                y = randint(0, 128)
            self.monster_list.append(Monster(x, y, 16, 16, 1, 1))
                
    def update(self, m_list):
        self.monster_list = m_list
        self.spawn()
        return self.monster_list
        
                