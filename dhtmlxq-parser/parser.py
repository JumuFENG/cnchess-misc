# Python 3
# -*- coding: utf-8 -*-

class ChessPos():
    def __init__(self, x = -1, y = -1):
        self.x = x
        self.y = y

class ChessItem():
    def __init__(self, id, name, pos = None):
        self.id = id
        self.name = name
        self.pos = ChessPos() if pos is None else pos
        
    def move_to(pos):
        self.pos = pos

class Parser():
    def __init__(self):
        self.all_chess = []

    def init(self, binit = None):
        if not isinstance(binit, str) or not len(binit) == 64:
            binit = '8979695949392919097717866646260600102030405060708012720323436383'

        print([p for p in binit[::2] ])
        

    def load_dhtml(self, text):
        pass
        
if __name__ == '__main__':
    p = Parser()
    p.init()