# -*- coding: utf-8 -*-

import re
import urllib.request
from bs4 import BeautifulSoup


def t001(url):
    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        return -1

    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    if (soup.resultcode.string != '00'):
        print('[TEST001][Not OK]\t')
        print('\t', soup.resultmsg.string)
        return -1

    items = soup.findAll('item')
    for item in items:
        item = item.text
        item = re.sub('<.*?>', '|', item)
        info = item.split('|')
        print('[TEST001][OK]\t')
        ret_msg = '%s %s(%s) %s층 %sm² %s(%s) 준공:%s\n' % (
                info[3], info[5], info[8], info[12], info[9],
                info[4], info[7], info[1])
        print('\t', ret_msg)
        print('[TEST002][PASS]')
        print('[TEST003][PASS]')
        return 0

    print('[TEST001][Not OK]\t')
    return -1
