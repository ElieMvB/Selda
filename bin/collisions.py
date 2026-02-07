import pyxel

class Collisions:
    def __init__(self):
        pass
    
    def colliderect(self, r1, r2):
        '''
        in:
            2 lists that represent hit boxes (ex : [x, y, width, height])
            the list can have more than four elements, but only the first four will be taken in account
        out: 
            True if hit boxes collide
            False else
        '''
        if ((r2[0] < r1[0] + r1[2]) and (r2[0] + r2[2] > r1[0])) and ((r2[1] < r1[1] + r1[3]) and (r2[1] + r2[3] > r1[1])):
            return True
        return False
    
    def intrusion(self, r1, r2):
        '''
        in:
            2 rectangles ([x, y, widht, height])
        out:
            int x, int y
            the movement that should do the first rectangle to go away from the second one if they collide
        '''
        dx = r1[0] + (r1[2] // 2) - (r2[0] + (r2[2] // 2))
        dy = r1[1] + (r1[3] // 2) - (r2[1] + (r2[3] // 2))
        if dx <= 0:
            x = -(r1[0] + r1[2] - r2[0])
        else:
            x = r2[0] + r2[2] - r1[0]
        if dy <= 0:
            y = -(r1[1] + r1[3] - r2[1])
        else:
            y = r2[1] + r2[3] - r1[1]
        if dx > 0 or dy > 0:
            if abs(dx) < abs(dy):
                return 0, y
            elif abs(dx) > abs(dy):
                return x, 0
        else:
            if dx > dy:
                return 0, y
            elif dx < dy:
                return x, 0
        return x, y
    
    def move_test(self, rd, r1, lr, dx, dy):
        '''
        in:
            the main rectangle in movement
            list of rects around an hit box
            list of rect to not touch
            deplacement on x and y
        out:
            new x and y to avoid the rects in the list of rects to not touch
        '''
        for r in lr:
            if self.colliderect(rd, r):
                #si la coordonée est pas multiple de la vitesse ça ne marche pas
                #cette condition permer de dégager les rects qui ne deuvent pas être ensembles
                print(self.intrusion(rd, r))
                return self.intrusion(rd, r)
            else:
                if self.colliderect(r1[0], r):
                    if dy < 0:
                        dy = 0
                if self.colliderect(r1[1], r):
                    if dy > 0:
                        dy = 0
                if self.colliderect(r1[2], r):
                    if dx < 0:
                        dx = 0
                if self.colliderect(r1[3], r):
                    if dx > 0:
                        dx = 0
                if self.colliderect(r1[4], r):
                    if dx < 0 and dy < 0:
                        dy = 0
                        dx = 0
                if self.colliderect(r1[5], r):
                    if dx < 0 and dy > 0:
                        dx = 0
                        dy = 0
                if self.colliderect(r1[6], r):
                    if dx > 0 and dy < 0:
                        dy = 0
                        dx = 0
                if self.colliderect(r1[7], r):
                    if dx > 0 and dy > 0:
                        dy = 0
                        dx = 0
        return dx, dy
