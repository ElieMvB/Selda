import pyxel
from bin.entity import*

class Arrow(Entity):
    def __init__(self, x, y, w, h, s, d, pr):
        super().__init__(x, y, w, h, s)
        if d[0] == 1:
            x += pr[2]
        if d[1] == 1:
            y += pr[3]
        self.velocity = d
        self.u = 8 + 8 * d[0]
        self.v = 8 + 8 * d[1]
        
    def draw(self):
        pyxel.blt(self.rect[0], self.rect[1], 0, self.u, self.v, 8, 8, 2)
