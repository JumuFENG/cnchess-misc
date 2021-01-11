# Python 3
# -*- coding: utf-8 -*-

from netutil.netutils import XQDownloader
from xqparser.dhtmlxq import Parser
from db_utils import ChessDb
import re

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
    start = '/Category/View-8288.html'
    nexthref = get_next_view(start, category)
    while repeat:
        nexthref = get_next_view(nexthref, category)
        if nexthref == '/':
            break

def get_from_db():
    db = ChessDb()
    p = Parser()
    qp = db.get_all_qipu()
    for x in qp:
        p.translate(x)

if __name__ == '__main__':
    #get_views()
    get_from_db()