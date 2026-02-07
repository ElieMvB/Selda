import pyxel
from bin.entity import*
from bin.arrow import*

class Player(Entity):
    def __init__(self, x, y, w, h, s):
        super().__init__(x, y, w, h, s)
        self.attack = 0
        self.power = 5
        self.frame_count = 0
        self.anim_coeff = 0
        self.cy = 2
        self.cx = 0
        self.shield = 5
        self.shield_heal_anim = 0
        self.health = 3
        self.invisibility = 0
        self.arrow_list = []
        self.quiver = 10
        
    def get_input(self):
        #gets the player inputs
        if self.invisibility == 0:
            self.velocity = [0, 0]
        if pyxel.btn(pyxel.KEY_LEFT):
            self.velocity[0] = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.velocity[0] = 1
        if pyxel.btn(pyxel.KEY_UP):
            self.velocity[1] = -1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.velocity[1] = 1
        
        self.get_direction()
        
        if self.attack == 0:
            if pyxel.btnr(pyxel.KEY_SPACE) and self.attack == 0 and self.quiver > 0:
                self.attack = 1
                self.arrow_list.append(Arrow(self.rect[0], self.rect[1], 8, 8, 3, self.direction, self.rect))
                self.quiver -= 1
    
    def animation(self):
        if self.direction[0] == -1:
            self.cy = 2
        elif self.direction[0] == 1:
            self.cy = 0
        elif self.direction[1] == -1:
            self.cy = 1
        elif self.direction[1] == 1:
            self.cy = 3
        if self.velocity == [0, 0]:
            self.cx = 48
        else:
            self.frame_count += 1
            if self.frame_count >= 5:
                self.frame_count = 0
                self.cx = 32 + 8 * self.anim_coeff
                if self.anim_coeff == 0:
                    self.anim_coeff = 1
                else:
                    self.anim_coeff = 0
        if self.shield_heal_anim > 0:
            self.shield_heal_anim += 1
            if self.shield_heal_anim >= 10:
                self.shield_heal_anim = 0
    
    def kb(self, att_r):
        #handles knock back when the player gets damaged
        #not the same one of the monster
        if att_r[0] > self.rect[0]:
            self.velocity[0] = -1
        elif att_r[0] < self.rect[0]:
            self.velocity[0] = 1
        else:
            self.velocity[0] = 0
        if att_r[1] > self.rect[1]:
            self.velocity[1] = -1
        elif att_r[1] < self.rect[1]:
            self.velocity[1] = 1
        else:
            self.velocity[1] = 0
        self.invisibility = 1
        
    def damage(self, d, ar):
        if self.invisibility == 0:
            pyxel.play(2, 63)
            if self.shield > 0:
                self.shield -= d
            else:
                self.health -= 1
            if self.shield < 0:
                self.shield = 0
            self.kb(ar)
            
    def heal_shield(self):
        self.shield += 1
        self.shield_heal_anim += 1
        pyxel.play(2, 62)
    
    def update(self):
        self.get_input()
        if self.attack != 0:
            self.attack += 1
            if self.attack >= 5:
                self.attack = 0
        else:
            self.borders()
            self.move()
        self.animation()
        if self.invisibility > 0:
            self.invisibility += 1
            if self.invisibility >= 30:
                self.invisibility = 0
        for a in self.arrow_list:
            a.move()
        return (self.attack, self.arrow_list)
    
    def draw(self):
        if self.invisibility > 0:
            pyxel.blt(self.rect[0], self.rect[1], 0, self.cx + 24, self.cy * 8 + 88, 8, 8, 0)
        elif self.shield_heal_anim > 0:
            pyxel.blt(self.rect[0], self.rect[1], 0, self.cx + 48, self.cy * 8 + 88, 8, 8, 0)
        else:
            pyxel.blt(self.rect[0], self.rect[1], 0, self.cx, self.cy * 8 + 88, 8, 8, 0)
        if self.attack != 0 and self.attack <= 4:
            pyxel.blt(self.rect[0] + 6 * self.direction[0], self.rect[1] + 6 * self.direction[1], 0, (self.attack - 1) * 8, 88 + 8 * self.cy, 8, 8, 2)
        for a in self.arrow_list:
            a.draw()
