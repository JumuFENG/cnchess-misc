# Python 3
# -*- coding: utf-8 -*-

import re

class ChessPos():
    def __init__(self, x = -1, y = -1, xy = None):
        self.set_pos(x, y, xy)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

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
        if self.x > 8 or self.y > 9 or self.x < 0 or self.y < 0:
            self.x = -1
            self.y = -1

class ChessItem():
    def __init__(self, id, name, pos = None):
        self.id = id
        self.name = name
        self.pos = ChessPos() if pos is None else pos
        
    def __str__(self):
        return self.name + str(self.pos)

    def move_to(self, pos):
        self.pos = ChessPos() if pos is None else pos        

class ChessStep():
    def __init__(self, step, comment = None, desc = None):
        self.step = step
        self.comment = comment
        self.desc = desc
        self.src = ChessPos(xy = step[0:2])
        self.dest = ChessPos(xy = step[2:4])

    def __str__(self):
        return self.step if self.desc is None else self.desc

    def full_step(self):
        return self.__str__() if self.comment is None else self.__str__() + '  ' + self.comment

class Parser():
    def __init__(self, show_comments = True):
        self.show_comments = show_comments
        self.all_chess = [
            ChessItem('rR1','车'), ChessItem('rH1','马'), ChessItem('rE1','相'), ChessItem('rA1','仕'), 
            ChessItem('rK','帅'), ChessItem('rA2','仕'), ChessItem('rE2','相'), ChessItem('rH2','马'),
            ChessItem('rR2','车'), ChessItem('rC1','炮'), ChessItem('rC2','炮'), ChessItem('rP1','兵'), 
            ChessItem('rP2','兵'), ChessItem('rP3','兵'), ChessItem('rP4','兵'), ChessItem('rP5','兵'),
            ChessItem('bR1','车'), ChessItem('bH1','马'), ChessItem('bE1','象'), ChessItem('bA1','士'), 
            ChessItem('bK','将'), ChessItem('bA2','士'), ChessItem('bE2','象'), ChessItem('bH2','马'),
            ChessItem('bR2','车'), ChessItem('bC1','炮'), ChessItem('bC2','炮'), ChessItem('bP1','卒'), 
            ChessItem('bP2','卒'), ChessItem('bP3','卒'), ChessItem('bP4','卒'), ChessItem('bP5','卒'),
        ]

        self.line_labels = ['九', '八', '七', '六', '五', '四', '三', '二', '一']

    def init(self, binit = None):
        if not isinstance(binit, str) or not len(binit) == 64:
            binit = '8979695949392919097717866646260600102030405060708012720323436383'

        iinit = [ChessPos(xy = binit[i: i+2]) for i in range(0, len(binit), 2)]

        if not len(iinit) == len(self.all_chess):
            print("input error!")
            return

        for i in range(0, len(iinit)):
            self.all_chess[i].move_to(iinit[i])

    def get_chess_by_pos(self, pos):
        for c in self.all_chess:
            if c.pos.x == pos.x and c.pos.y == pos.y:
                return c

    def get_same_chess_vline(self, c):
        cs = []
        for x in self.all_chess:
            if x.id[0] == c.id[0] and x.name == c.name and x.pos.x == c.pos.x and not x.pos.y == c.pos.y:
                cs.append(x)
        return cs

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

    def get_front_end_str(self, c, others):
        if not isinstance(others, list):
            print('make sure the others are a list')
            return

        fe = ''
        y = c.pos.y
        if len(others) == 1:
            o = others[0]
            if c.id[0] == 'r':
                fe = '后' if y > o.pos.y else '前'
            else:
                fe = '后' if y < o.pos.y else '前'
            if c.id[1] == 'P':
                fe += c.name + self.get_line_label(c.id, c.pos)
            else:
                fe += c.name
            return fe
        if len(others) == 2:
            y1 = others[0].pos.y
            y2 = others[1].pos.y
            if y > y1 and y > y2:
                fe = '后' if c.id[0] == 'r' else '前'
            elif y < y1 and y < y2:
                fe = '前' if c.id[0] == 'r' else '后'
            else:
                fe = '中'
            return fe + c.name + self.get_line_label(c.id, c.pos)
        else:
            others.sort(key = lambda o: o.pos.y)
            max_y = others[-1].pos.y
            min_y = others[0].pos.y
            if y > max_y:
                fe = '后' if c.id[0] == 'r' else '前'
            elif y < min_y:
                fe = '前' if c.id[0] == 'r' else '后'
            else:
                lty = sum(1 for o in others if o.pos.y < y)
                fe = self.line_labels[-lty-1] if c.id[0] == 'r' else str(len(others) - lty + 1)
            return fe + c.name + self.get_line_label(c.id, c.pos)

    def get_distance_str(self, cid, y1, y2):
        if cid[0] == 'r':
            return self.line_labels[-abs(y1 - y2)]
        return str(abs(y1 - y2))

    def translate_step(self, step):
        pos1 = step.src
        pos2 = step.dest
        c = self.get_chess_by_pos(pos1)
        if c is None:
            print('no chess located in pos: ', pos1.x, pos1.y)
            return
        co = self.get_same_chess_vline(c)
        stp = ''
        if len(co) > 0:
            stp = self.get_front_end_str(c, co)
        else:
            stp = c.name + self.get_line_label(c.id, pos1)
        if pos1.y == pos2.y:
            stp += '平' + self.get_line_label(c.id, pos2)
        else:
            stp += self.get_dir_str(c.id, pos1.y, pos2.y)
            if pos1.x == pos2.x:
                stp += self.get_distance_str(c.id, pos1.y, pos2.y)
            else:
                stp += self.get_line_label(c.id, pos2)

        rstp = step
        rstp.desc = stp
        d = self.get_chess_by_pos(pos2)
        if d is not None:
            d.move_to(None)
        c.move_to(pos2)
        return rstp

    def translate_steps(self, steps):
        self.init()
        stps = [self.translate_step(s) for s in self.get_whole_steps(self.step_lists, steps['id'])]
        str_step_all = []
        for i in range(0, len(stps), 2):
            str_step = str(int(1 + i/2)) + ': '
            if i + 1 == len(stps):
                str_step += stps[i].full_step() if self.show_comments else str(stps[i])
                str_step_all.append(str_step)
                continue
            if not self.show_comments:
                str_step += str(stps[i]) + '  ' + str(stps[i+1])
            else:
                if stps[i].comment is None:
                    str_step += stps[i].full_step() + '  ' + stps[i+1].full_step()
                else:
                    str_step += stps[i].full_step()
                    str_step += '\n' + str(int(1 + i/2)) + ': ......   '
                    str_step += stps[i+1].full_step()
            str_step_all.append(str_step)
        steps['translated'] = str_step_all
            
    def get_whole_steps(self, step_lists, id):
        basestep = [s for s in step_lists if s['id'] == int(id)][0]
        if int(id) == 0 or basestep['id'] == basestep['baseid']:
            return basestep['steps']
        basesteps = self.get_whole_steps(step_lists, basestep['baseid'])
        return basesteps[0:basestep['start_node'] - 1] + basestep['steps']

    def match_step_comment(self, mvlist, comments):
        self.step_lists = []
        for m in mvlist:
            step = {}
            step['id'] = m['id']
            step['baseid'] = m['baseid']
            step['start_node'] = m['start_node']
            step['steps'] = [ChessStep(m['steps'][i:i+4]) for i in range(0,len(m['steps']),4)]
            for i in range(0, len(step['steps'])):
                comment = None
                for c in comments:
                    if c['step_list_id'] == m['id'] and c['step'] == i + m['start_node']:
                        comment = c['comment']
                        break
                step['steps'][i].comment = comment
            self.step_lists.append(step)

    def load_dhtml(self, text):
        chess_game = {'move_list':[], 'comments':[]}
        cmts = re.findall(r'\[DhtmlXQ_comment([\d]+)\](.*?)\[/DhtmlXQ_comment([\d]+)\]', text, re.DOTALL)
        [chess_game['comments'].append({'step_list_id':0, 'step':int(c[0]), 'comment': c[1]}) for c in cmts if c[0] == c[2]]
        cmts = re.findall(r'\[DhtmlXQ_comment([\d]+)_([\d]+)\](.*?)\[/DhtmlXQ_comment([\d]+)_([\d]+)\]', text, re.DOTALL)
        [chess_game['comments'].append({'step_list_id':int(c[0]), 'step':int(c[1]), 'comment': c[2]}) for c in cmts if c[0] == c[3] and c[1] == c[4]]
        title = re.search(r'\[DhtmlXQ_title\](.*?)\[/DhtmlXQ_title\]', text).group(1).strip()
        chess_game['title'] = title
        binit = re.search(r'\[DhtmlXQ_binit\](.*?)\[/DhtmlXQ_binit\]', text).group(1).strip()
        chess_game['binit'] = None if binit == '8979695949392919097717866646260600102030405060708012720323436383' else binit
        mvlist = re.search(r'\[DhtmlXQ_movelist\](.*?)\[/DhtmlXQ_movelist\]', text).group(1).strip()
        chess_game['move_list'].append({'id': 0, 'steps': mvlist, 'baseid': 0, 'start_node':1})
        sublist = re.findall(r'\[DhtmlXQ_move_([\d]+)_([\d]+)_([\d]+)\](.*?)\[/DhtmlXQ_move_([\d]+)_([\d]+)_([\d]+)\]', text, re.DOTALL)
        [chess_game['move_list'].append({
            'id':int(s[2]), 'steps':s[3], 'baseid': int(s[0]), 'start_node':int(s[1])
            }) for s in sublist if s[0] == s[4] and s[1] == s[5] and s[2] == s[6]]
        return chess_game

    def translate(self, chess_game):
        self.match_step_comment(chess_game['move_list'], chess_game['comments'])
        [self.translate_steps(s) for s in self.step_lists]
        for m in chess_game['move_list']:
            for s in self.step_lists:
                if m['id'] == s['id']:
                    m['translated'] = s['translated']
                    break

if __name__ == '__main__':
    pos = ChessPos(xy ='12')
    print(pos)
    chs = ChessItem('rR1','车')
    print(chs)
    chs.move_to(pos)
    print(chs)
    step = ChessStep('1122')
    print(step)
    step.desc = 'j1j1'
    print(step)
    step.comment = 'comment'
    print(step.full_step())
