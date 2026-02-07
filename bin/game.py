import pyxel
from time import sleep
from bin.collisions import*
from bin.player import*
from bin.waves_manager import*
from bin.text_manager import*
from bin.items import*

class Game:
    def __init__(self):
        self.pause = True
        
        self.time_win = 0
        self.die_monsters = 0
        self.wave_num =0.5 #integers are for actual waves, non integers are for scenario
        self.wave_attack = [1, 2, 3, 4, 5]
        self.wave_stories = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        
        self.collisions = Collisions()
        self.text = TextManager()
        self.player = Player(50, 50, 8, 8, 2)
        self.items = Items()
        self.wave = Waves(1)
        self.monster_list = []
        
        self.background = {'1': {'fond': [(128, 1408), (128, 1408)], 'add': [(256, 1408)], 'ground': []}, '2': {'fond': [(128, 1536), (256, 1536)],'add': [], 'ground': [(384, 1536)]}}
        self.background['3'] = {'fond': [(128, 1664), (256, 1664)], 'add': [], 'ground': []}
        self.background['4'] = {'fond': [(128, 1792), (256, 1792)], 'add': [], 'ground': []}
        self.background['5'] = {'fond': [(128, 1920), (128, 1920)], 'add': [(256, 1920)], 'ground': []}
        self.back_anim = 0
        
        self.stories_text = {'1': "Le chateau est attaque! Vite! Il faut le deffendre!$Toi, valeureux guerrier, bats-toi pour le chateau!"}
        self.stories_text['2'] = "Tu ne pourras pas passer par l'entree... Tu vas devoir passer par les egouts pour rejoindre le roi et le proteger."
        self.stories_text['3'] = "Bravo tu avance bien!$Mais l'ennemi est extremement infiltre... Il vas te falloir du courrage et de la force!"
        self.stories_text['4'] = "Tu a vraimment reussi?! Super! Mais le plus dur reste a venir... $Tu dois desormais rentrer dans les quartiers royaux."
        self.stories_text['5'] = "Enfin dans les quartiers royaux! Il ne reste plus que a tuer les derniers ennemis et le roi sera sauve! Tout repose sur toi maintenant."
        self.stories_text['6'] = "Le roi est sauve! Et tout ca grace a toi. Merci infiniment!$$Jeux de Elie et Manoe :)"
        
        pyxel.stop()
        pyxel.playm(6)
        
    def coli(self):
        #handles collisions
        #handles collisions withs monsters
        for m in self.monster_list:
            s = False
            if self.collisions.colliderect(self.player.rect, m.see_rect):
                s = True
            m.update(s, self.player.rect)
            if self.collisions.colliderect(self.player.rect, m.rect):
                self.player.damage(m.power, m.rect)
            for a in self.player.arrow_list:
                if self.collisions.colliderect(m.rect, a.rect):
                    m.damage(self.player.power, a.rect)
                    if m.health <= 0:
                        if m in self.monster_list:
                            self.items.spawn((m.rect[0], m.rect[1]))
                            self.monster_list.remove(m)
                            self.die_monsters += 1
                    if a in self.player.arrow_list:
                        self.player.arrow_list.remove(a)
            if self.player.health <= 0:
                return True
        #handles collisions with items (arrows and shilds)
        for a in self.items.arrow_list:
            if self.collisions.colliderect(self.player.rect, a.rect):
                pyxel.play(2, 59) #mettre 59
                self.player.quiver += 5
                self.items.arrow_list.remove(a)
        for s in self.items.shield_list:
            if self.collisions.colliderect(self.player.rect, s.rect):
                if self.player.shield < 10:
                    self.player.heal_shield()
                    self.items.shield_list.remove(s)
        
    def update(self):
        #upodates the state of the game
        out = False
        if self.wave_num in self.wave_stories: #shows only text because wahe is not an integer
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.wave_num += 0.5
                self.wave_num = int(self.wave_num)
                self.wave = Waves(self.wave_num)
                self.monster_list = []
                self.items = Items()
                pyxel.stop()
                pyxel.playm(self.wave_num, loop=True)
                
        else: #real wave of ennemies
            if self.pause:
                player_att = self.player.update()
                out = self.coli()
                if self.time_win == 0:
                    self.monster_list = self.wave.update(self.monster_list)
                self.items.spawn()
                #conditions to stop the game and let a bit of time to the player after each wave
                #this time is counter by time_win
                if self.die_monsters >= 2 * self.wave_num:
                    pyxel.stop()
                    pyxel.play(1, 58)
                    self.die_monsters = 0
                    self.monster_list = []
                    self.time_win = 1
                if self.time_win > 0:
                    self.time_win += 1
                if self.time_win >= 60:
                    self.wave_num += 0.5 
                    self.die_monsters = 0
                    self.time_win = 0
                    pyxel.stop()
                    if self.wave_num == 5.5: #the end of the game
                        pyxel.playm(7, loop=True)
                    else:
                        pyxel.playm(6, loop=True)
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.pause = not(self.pause)
        if self.wave_num == 6:
            out = True
        return out
    
    def draw_back1(self):
        #displays what is behind the player, monsters and items
        if pyxel.frame_count % 15 == 0:
            self.back_anim += 1 + (self.back_anim * -2)
        lf = self.background[str(self.wave_num)]['fond']
        pyxel.bltm(0, 0, 0, lf[self.back_anim][0], lf[self.back_anim][1], 128, 128)
        if len(self.background[str(self.wave_num)]['ground']) != 0:
            for e in self.background[str(self.wave_num)]['ground']:
                pyxel.bltm(0, 0, 0, e[0], e[1], 128, 128, 2)
        
    def draw_back2(self):
        #diplays what is in front of the player
        if len(self.background[str(self.wave_num)]['add']) == 1:
            pyxel.bltm(0, 0, 0, self.background[str(self.wave_num)]['add'][0][0], self.background[str(self.wave_num)]['add'][0][1], 128, 128, 2)
    
    def display(self):
        #diplayse every thing on the screen
        if self.wave_num in self.wave_attack and self.pause:
            self.draw_back1()
            self.items.draw()
            for m in self.monster_list:
                m.draw()
            self.player.draw()
            self.draw_back2()
            for i in range(self.player.health):
                pyxel.blt(3 + (10 * i), 15, 0, 0, 80, 8, 8, 2)
            for i in range(self.player.shield):
                pyxel.blt(3 + (10 * i), 5, 0, 8, 80, 8, 8, 2)
            if self.player.quiver > 0:
                pyxel.blt(5, 117, 0, 48, 128, 8, 8, 2)
            else:
                pyxel.blt(5, 117, 0, 56, 128, 8, 8, 2)
            pyxel.text(5, 117, str(self.player.quiver), 0)
        elif self.wave_num in self.wave_stories:
            self.text.print_t(self.stories_text[str(self.wave_num + 0.5)[0]], (10, 7), 1)
        if not(self.pause):
            self.text.print_t("Pause", (40, 10), 1)
            self.text.print_t("Appuyez sur 'entre' pour relancer", (10, 40), 1)
        
