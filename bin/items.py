import pyxel
from bin.entity import*
from random import randint

class Items:
    def __init__(self):
        self.arrow_list = []
        self.shield_list = []
        
    def spawn(self, it=None):
        if it is None:
            if pyxel.frame_count % 30 == 0 and randint(0, 5) == 0:
                self.arrow_list.append(Entity(randint(0, 120), randint(0, 120), 8, 8, 0))
        else:
            self.shield_list.append(Entity(it[0], it[1], 8, 8, 0))
            
    def draw(self):
        for a in self.arrow_list:
            pyxel.blt(a.rect[0], a.rect[1], 0, 16, 0, 8, 8, 2)
        for s in self.shield_list:
            pyxel.blt(s.rect[0], s.rect[1], 0, 8, 80, 8, 8, 2)