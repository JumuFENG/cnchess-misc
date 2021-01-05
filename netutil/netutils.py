# Python 3
# -*- coding: utf-8 -*-

import requests

class XQDownloader():
    def __init__(self):
        self.Host = 'www.xiangqiqipu.com'
        self.schema = 'https'

    def get_request(self, filename = None, url = None):
        headers = {
            'Host': self.Host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        params=None
        proxies=None

        if url is None:
            url = self.schema + '://' + self.Host + filename
            
        rsp = requests.get(url, headers=headers, params=params, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text
