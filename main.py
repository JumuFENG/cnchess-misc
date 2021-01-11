# Python 3
# -*- coding: utf-8 -*-

from netutil.netutils import XQDownloader
from xqparser.dhtmlxq import Parser
from db_utils import ChessDb
import re

def get_next_view(fn):
    d = XQDownloader()
    html = d.get_request(fn)

    p = Parser()
    db = ChessDb()
    dhtml = re.findall(r'\[DhtmlXQ\](.*?)\[/DhtmlXQ\]', html, re.DOTALL)
    for h in dhtml:
        game = p.load_dhtml(h)
        db.save_game(game)
        p.translate(game)
    nexthref = re.search(r'<a href="(.*?)" class="next">下局棋谱：', html).group(1).strip()
    print('next: ', nexthref)
    return nexthref

def get_views(start, repeat = False):
    nexthref = get_next_view(start)
    while repeat:
        nexthref = get_next_view(nexthref)
        if nexthref == '/':
            break

def get_from_db():
    db = ChessDb()
    p = Parser()
    qp = db.get_all_qipu()
    for x in qp:
        p.translate(x)

if __name__ == '__main__':
    #get_views('/Category/View-8288.html')
    get_from_db()