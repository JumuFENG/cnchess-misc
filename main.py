# Python 3
# -*- coding: utf-8 -*-

from netutil.netutils import XQDownloader
from xqparser.dhtmlxq import Parser
from db_utils import ChessDb
import re
import os

def get_next_view(fn, cat):
    d = XQDownloader()
    html = d.get_request(fn)
    title = re.search(r'<title>(.*?)</title>', html).group(0).strip()

    p = Parser()
    db = ChessDb()
    dhtml = re.findall(r'\[DhtmlXQ\](.*?)\[/DhtmlXQ\]', html, re.DOTALL)
    for h in dhtml:
        game = p.load_dhtml(h)
        game['category'] = cat
        if title is not None:
            game['tips'] = title.split('：')[0]
        db.save_game(game)
    nexthref = re.search(r'<a href="(.*?)" class="next">下局棋谱：', html).group(1).strip()
    print('next: ', nexthref)
    return nexthref

def get_all_jzm():
    category = '橘中秘'
    start = '/Category/View-8261.html'
    nexthref = get_next_view(start, category)
    while True:
        nexthref = get_next_view(nexthref, category)
        print(nexthref)
        if nexthref == '/':
            break

def get_all_mhp():
    category = '梅花谱'
    start = '/Category/View-8052.html'
    nexthref = get_next_view(start, category)
    while True:
        nexthref = get_next_view(nexthref, category)
        print(nexthref)
        if nexthref == '/':
            break

def get_from_db():
    db = ChessDb()
    p = Parser(False)
    t = db.get_qipu(82)
    p.translate(t)
    for x in t['move_list']:
        print(t['title'] + ' 本变：' if x['id'] == 0 else t['title'] + ' ' + str(x['id']) + '变：')
        for s in x['translated']:
            print(s)

def dump_to_file(id, file):
    db = ChessDb()
    t = db.get_qipu(id)
    p = Parser(False)
    p.translate(t)
    txt = []
    for x in t['move_list']:
        txt.append('<h2>' + t['tips'] + t['title'] + '</h2>' if x['id'] == 0 else '')
        ml = '本变' if x['id'] == 0 else str(x['id']) + '变'
        txt.append('<h3 style="text-align:center">' + ml + '</h3>')
        for s in x['translated']:
            txt.append(s + '</br>')

    with open(file, 'wt', encoding='utf-8') as f:
        for s in txt:
            f.write('%s\n' % s)

def load_single_qipu():
    txt = """
    """
    if len(txt) < 10:
        raise Exception('please set dhtml to txt')
    p = Parser()
    game = p.load_dhtml(txt)
    game['id'] = 29
    game['category'] = '橘中秘'
    game['tips'] = '让先'
    game['title'] = '009小列手破大列手炮局'
    db = ChessDb()
    db.save_game(game)

def fix_data_in_db():
    db = ChessDb()
    mhtips = db.db.select('chess_qipu', ['id', 'tips'], 'category = "梅花谱"')
    for t in mhtips:
        t['tips'] = t['tips'].split('<title>')[1]

    db.db.update_many('chess_qipu', conkeys=['id'], datalist = mhtips)
    print('done!')

if __name__ == '__main__':
    # get_views()
    # get_from_db()
    # get_all_jzm()
    dump_to_file(3, '1.html')
