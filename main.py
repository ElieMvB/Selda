import pyxel
from bin.menu import*
from bin.game import*

class Main:
    def __init__(self):
        pyxel.init(128, 128, title="Selda")
        pyxel.load("assets/assets.pyxres")
        
        self.menu = Menu()

        self.state = 'menu'
         
        #main loop
        pyxel.run(self.update, self.display)
        
    def update(self):
        if self.state == 'menu':
            if self.menu.update():
                self.state = 'game'
                pyxel.stop()
                self.game = Game()
        elif self.state == 'game':
            end = self.game.update()
            if end:
                self.state = 'game_over'
                pyxel.stop()
        elif self.state == 'game_over':
            if pyxel.btnr(pyxel.KEY_SPACE):
                self.state = 'menu'
                pyxel.stop()
                self.menu = Menu()
    
    def display(self):
        pyxel.cls(0)
        if self.state == 'menu':
            self.menu.draw()
        elif self.state == 'game':
            self.game.display()
        elif self.state == 'game_over':
            pyxel.text(50, 50, 'GAME OVER !', 10)
            pyxel.text(1, 60, 'appuyez sur espace pour relancer', 10)
        
pgm = Main()