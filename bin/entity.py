import pyxel

class Entity:
    def __init__(self, x, y, w, h, s):
        '''
        in:
            x and y coords
            width and height
            speed
        '''
        self.speed = s
        self.velocity = [0, 0]
        self.rect = [x, y, w, h]
        #rect au tour du vrai rect: (basés sur le 'main' des collisions)
        self.col_rect = [[x, y-1, w, 1, 3], [x, y+h, w, 1, 3], [x-1, y, 1, h, 3], [x+w, y, 1, h, 3], [x-1, y-1, 1, 1, 11], [x-1, y+h, 1, 1, 11], [x+w, y-1, 1, 1, 11], [x+w, y+h, 1, 1, 11]]
        self.direction = [0, -1]

    def move(self):
        #move the entity with its speed and velocity
        self.rect[0] += self.velocity[0] * self.speed
        self.rect[1] += self.velocity[1] * self.speed
        for r in self.col_rect:
            r[0] += self.velocity[0] * self.speed
            r[1] += self.velocity[1] * self.speed
        
    def tp(self, x, y):
        #places the entity at the coord (x, y)
        self.rect[0] = x
        self.rect[1] = y
        
    def get_direction(self):
        if self.velocity != [0, 0]:
            if self.velocity[0] == 0:
                self.direction = [0, self.velocity[1]]
            else:
                self.direction = [self.velocity[0], 0]
                
    def borders(self):
        #avoid going out of screen
        v = self.velocity
        if self.rect[0] + self.rect[2] >= 128:
            self.velocity[0] = -1
            self.rect[0] = 128 - self.rect[2]
        if self.rect[0] <= 0:
            self.velocity[0] = 1
            self.rect[0] = 0
        if self.rect[1] + self.rect[3] >= 128:
            self.velocity[1] = -1
            self.rect[1] = 128 - self.rect[3]
        if self.rect[1] <= 0:
            self.velocity[1] = 1
            self.rect[1] = 0
        if v == self.velocity:
            return False
        return True

        

        
