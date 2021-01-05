# Python 3
# -*- coding: utf-8 -*-

from netutil.netutils import XQDownloader
from xqparser.dhtmlxq import Parser
import re

def get_next_view(fn):
    d = XQDownloader()
    html = d.get_request(fn)

    p = Parser()
    dhtml = re.findall(r'\[DhtmlXQ\](.*?)\[/DhtmlXQ\]', html, re.DOTALL)
    [p.load_dhtml(h) for h in dhtml]
    nexthref = re.search(r'<a href="(.*?)" class="next">下局棋谱：', html).group(1).strip()
    return nexthref

def get_views(start, repeat = False):
    nexthref = get_next_view(start)
    while repeat:
        nexthref = get_next_view(nexthref)
        if nexthref == '/':
            break

if __name__ == '__main__':
    get_views('/Category/View-8289.html')
