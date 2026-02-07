import pyxel
from bin.entity import*
from random import randint

class Monster(Entity):
    def __init__(self, x, y, w, h, s, lvl):
        super().__init__(x, y, w, h, s)
        self.power = 3 + 2 * (lvl - 1)
        self.y = 128 * lvl
        self.anim_state = 0
        self.see_rect = [x, y, w, h]
        self.original_speed = self.speed
        self.health = 15
        self.invisibility = 0
    
    def kb(self, att_r):
        #give knock back to the ennemy when damaged
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
        self.speed = self.original_speed * 2
        
    def damage(self, d, ar):
        if self.invisibility == 0:
            self.health -= d
            self.kb(ar)
            pyxel.play(3, 61)
    
    def attack_move(self):
        pass
    
    def ai_move(self, see_player, rect_player):
        if see_player:
            self.speed = self.original_speed * 2
            self.attack_move()
        else:
            self.speed = self.original_speed
            b = self.borders()
            if randint(0, 60) == 0 and not(b):
                self.velocity = [randint(-1, 1), randint(-1, 1)]
                
    def anim(self):
        if pyxel.frame_count % 10 == 0:
            self.anim_state += 1
            if self.anim_state >= 3:
                self.anim_state = 0
                
    def update(self, see_player, player_rect):
        self.anim()
        self.get_direction()
        if self.invisibility == 0:
            self.see_rect = [self.rect[0] + (16 * self.direction[0]) - 4, self.rect[1] + (16 * self.direction[1]) - 4, 24, 24]
            self.ai_move(see_player, player_rect)
        else:
            self.invisibility += 1
            if self.invisibility >= 10:
                self.invisibility = 0
        self.move()
    
    def draw(self):
        if self.invisibility == 0:
            pyxel.blt(self.rect[0], self.rect[1], 0, self.rect[2] * self.anim_state, self.y , self.rect[2], self.rect[3], 6)
        else:
            pyxel.blt(self.rect[0], self.rect[1], 0, self.rect[2] * self.anim_state, self.y + 16, self.rect[2], self.rect[3], 6)
                