import pyxel

class TextManager:
    def __init__(self):
        #initalise all the characters of our fount in the .pyxres
        self.min = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
        self.maj = 'A?B?C?D?E?F?G?H?I?J?K?L?M?N?O?P?Q?R?S?T?U?V?W?X?Y?Z'.split('?')
        self.special1 = {' ': (208, 0), '.': (160, 48), '!': (168, 48), '?': (176, 48), '-': (200, 56), ',': (184, 48), '(': (208, 56), ')': (216, 56)}
        self.special1[':'] = (224, 56)
        self.special1["'"] = (192, 48)
        
    def get_i(self, t):
        '''
        in:
            t a list or a string containing the text to print
        out:
            cx and cy, two lists of lists containing the index of each character in their list
        '''
        cx = []
        cy = []
        tx = []
        ty = []
        for c in t:
            if c in self.min:
                tx.append(self.min.index(c))
                ty.append(0)
            elif c in self.maj:
                tx.append(self.maj.index(c))
                ty.append(1)
            elif c == ' ' or c == '$':
                tx.append(c)
                ty.append(c)
                cx.append(tx)
                cy.append(ty)
                tx = []
                ty = []
            else:
                tx.append(c)
                ty.append(c)
        cx.append(tx)
        cy.append(ty)
        tx = []
        ty = []
        return cx, cy
    
    def get_co(self, t, s=1):
        '''
        in:
            t a list or a string containing the text to print
            s should be the size, but for the moment it only can be 1
        out:
            a list containing the coords on the screen for every charcter
        '''
        cx, cy = self.get_i(t)
        co = []
        m_co = []
        if s == 1:
            for i in range(len(cx)):
                for j in range(len(cx[i])):
                    if type(cx[i][j]) == int: #simple charcter
                        m_co.append((cx[i][j] * 8, cy[i][j] * 8))
                    elif cx[i][j] == '$': #end of line
                        co.append(m_co)
                        m_co = []
                        co.append([(208, 0) for i in range(128)])
                    else: #'special' charcter (not a letter)
                        m_co.append(self.special1[cx[i][j]])
                co.append(m_co)
                m_co = []   
        return co
    
    def cha_x_max(self, co, s, xy):
        '''
        makes sure the text doesn't goes out of the screen by adding "returns to the line"
        in:
            the list of the coords, formed by get_co
            the size s (normally 1)
            xy the coords of the top lef of the text
        '''
        if s == 1: s=8
        elif s == 2: s=16
        else: s=32
        nc = (128 - xy[0]) // s
        
        l = []
        t = []
        lm = 0
        
        for m in co:
            lm += len(m)
            if lm <= nc:
                l.append(m)
            else:
                t.append(l)
                l = [m]
                lm = len(m)
        t.append(l)
        return t
            
        
    def print_t(self, t, xy, s=1):
        co = self.get_co(t, s)
        t = self.cha_x_max(co, s, xy)
        for i in range(len(t)):
            p = 0
            for j in range(len(t[i])):
                for k in range(len(t[i][j])):
                    pyxel.blt(xy[0] + 8 * p, xy[1] + 10 * i, 1, t[i][j][k][0], t[i][j][k][1], 8, 8, 0)
                    p += 1
