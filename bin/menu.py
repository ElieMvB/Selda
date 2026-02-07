import pyxel

class Menu:
    def __init__(self):
        self.animation = 0
        self.y = 0
        self.frame_count = 0
        self.color = 7
        pyxel.playm(0, loop=True)
    
    def update(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.animation = 1
        if self.animation == 0:
            if pyxel.frame_count % 30 == 0:
                if self.color == 7:
                    self.color = 6
                else:
                    self.color = 7
                
        elif self.animation == 1:
            self.y -= 2
            if self.y <= -90:
                self.animation = 2
        elif self.animation == 2:
            self.frame_count += 1
            if self.frame_count >= 100:
                return True
            
    
    def draw(self):
        pyxel.cls(12)
        pyxel.bltm(0, self.y, 0, 0, 1408, 128, 300, 2)
        if self.animation == 0:
            pyxel.text(25, 20, "Appuyez sur espace", self.color)
        elif self.animation == 2:
            pyxel.text(50, 50, "START !", 8)
        