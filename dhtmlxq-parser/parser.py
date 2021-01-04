# Python 3
# -*- coding: utf-8 -*-

class ChessPos():
    def __init__(self, x = -1, y = -1, xy = None):
        self.set_pos(x, y, xy)

    def set_pos(self, x = None, y = None, xy = None):
        if xy is None:
            self.x = int(x)
            self.y = int(y)
        elif isinstance(xy, str) and len(xy) == 2:
            self.x = int(xy[0])
            self.y = int(xy[1])
        elif isinstance(xy, int) and xy < 100 and xy > -1:
            self.x = xy / 10
            self.y = xy % 10

class ChessItem():
    def __init__(self, id, name, pos = None):
        self.id = id
        self.name = name
        self.pos = ChessPos() if pos is None else pos
        
    def move_to(self, pos):
        self.pos = pos

class Parser():
    def __init__(self):
        self.all_chess = [
            ChessItem('rR1','车'), ChessItem('rH1','马'), ChessItem('rE1','相'), ChessItem('rA1','仕'), 
            ChessItem('rK','帅'), ChessItem('rA2','仕'), ChessItem('rE2','相'), ChessItem('rH2','马'),
            ChessItem('rR2','车'), ChessItem('rC1','炮'), ChessItem('rC2','炮'), ChessItem('rP1','兵'), 
            ChessItem('rP2','兵'), ChessItem('rP3','兵'), ChessItem('rP4','兵'), ChessItem('rP5','兵'),
            ChessItem('gR1','车'), ChessItem('gH1','马'), ChessItem('gE1','象'), ChessItem('gA1','士'), 
            ChessItem('gK','将'), ChessItem('gA2','士'), ChessItem('gE2','象'), ChessItem('gH2','马'),
            ChessItem('gR2','车'), ChessItem('gC1','炮'), ChessItem('gC2','炮'), ChessItem('gP1','卒'), 
            ChessItem('gP2','卒'), ChessItem('gP3','卒'), ChessItem('gP4','卒'), ChessItem('gP5','卒'),
        ]

        self.line_labels = ['九', '八', '七', '六', '五', '四', '三', '二', '一']

    def init(self, binit = None):
        if not isinstance(binit, str) or not len(binit) == 64:
            binit = '8979695949392919097717866646260600102030405060708012720323436383'

        iinit = [ChessPos(x, y) for x,y in zip([int(i) for i in binit[::2]], [int(j) for j in binit[1::2]])]

        if not len(iinit) == len(self.all_chess):
            print("input error!")
            return

        for i in range(0, len(iinit)):
            self.all_chess[i].move_to(iinit[i])

    def get_chess_by_pos(self, pos):
        for c in self.all_chess:
            if c.pos.x == pos.x and c.pos.y == pos.y:
                return c

    def get_line_label(self, cid, pos):
        if cid[0] == 'r':
            return self.line_labels[pos.x]
        else:
            return str(pos.x + 1)

    def get_dir_str(self, cid, y1, y2):
        if y1 == y2:
            return '平'
        if cid[0] == 'r' :
            return '进' if y1 > y2 else '退'
        return '进' if y1 < y2 else '退'

    def get_distance_str(self, cid, y1, y2):
        if cid[0] == 'r':
            return self.line_labels[-(y1 - y2)]
        return str(abs(y1 - y2))

    def translate_step(self, step):
        pos1 = ChessPos(xy = step[0:2])
        pos2 = ChessPos(xy = step[2:4])
        c = self.get_chess_by_pos(pos1)
        if c is None:
            print('no chess located in pos: ', pos1.x, pos1.y)
        
        stp = c.name + self.get_line_label(c.id, pos1)
        if pos1.y == pos2.y:
            stp += '平' + self.get_line_label(c.id, pos2)
        else:
            stp += self.get_dir_str(c.id, pos1.y, pos2.y)
            if pos1.x == pos2.x:
                stp += self.get_distance_str(c.id, pos1.y, pos2.y)
            else:
                stp += self.get_line_label(c.id, pos2)

        c.move_to(pos2)
        return stp

    def translate_steps(self, steps):
        stps = [self.translate_step(steps[i:i+4]) for i in range(0,len(steps),4)]
        for s in stps:
            print(s)
            

    def load_dhtml(self, text):
        pass
        
if __name__ == '__main__':
    p = Parser()
    p.init()
    # 7747724279677062898880708838707638311002090812191712627047435041083840503130413038584252585250401242
    p.translate_steps('7747724279677062898880708838707638311002090812191712627047435041083840503130413038584252585250401242')

