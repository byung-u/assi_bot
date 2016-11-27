#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import re
from requests import get
from bs4 import BeautifulSoup

def t002():
    url = "http://www.naver.com/"
    r = get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    options = soup.find_all('option')
    realtime_rank = []

    for opt in options:
        opt = str(opt)
        m = re.search('>\d+위:', opt)
        if (m == None):
            continue
        idx = opt.find(">")
        opt = opt[idx+1:]
        realtime_rank.append(opt)

    if (len(realtime_rank) == 0):
        return -1

    print("[TEST002][OK]")
    print('\t', realtime_rank)
    return 0
